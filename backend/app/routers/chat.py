from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from typing_extensions import TypedDict, List
from pydantic import BaseModel
from langgraph.graph import START, StateGraph

load_dotenv()

# ENV config
env = os.getenv("ENV", "development")


# Embeddings setup
class HuggingFaceInferenceEmbeddings:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.token = os.getenv("HF_API_TOKEN")
        if not self.token:
            raise ValueError("HF_API_TOKEN not set in environment variables.")
        self.client = InferenceClient(token=self.token)
        self.model = model_name

    def embed_query(self, text: str):
        embedding = self.client.feature_extraction(text, model=self.model)
        return embedding.tolist() if hasattr(embedding, "tolist") else embedding


# Use LangChain's model in dev, custom in prod
if env == "production":
    embeddings = HuggingFaceInferenceEmbeddings()
else:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize Pinecone, embeddings, and Gemini model.
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_region = os.getenv("PINECONE_API_REGION", "us-east-1")
pinecone_index_name = os.getenv("PINECONE_API_INDEX", "document-index")
pc = Pinecone(api_key=pinecone_api_key)
pinecone_index = pc.Index(pinecone_index_name)

SYSTEM_PROMPT = (
    "You are AI Kostadin and you are a chatbot for Kostadin's personal website. "
    "Answer questions about him and his work. Do not answer unrelated or inappropriate questions. "
    "If context is provided and immediately relevant to the question, use it to inform your answer."
)


def get_gemini_model():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is not set in the environment variables.")
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
        api_key=api_key,
    )


def get_system_message():
    return SystemMessage(content=SYSTEM_PROMPT)


# Define models for conversation history.
class ChatMessage(BaseModel):
    role: str  # "system", "user", or "assistant"
    content: str


class QueryHistory(BaseModel):
    history: List[ChatMessage]

# LangGraph state


class State(TypedDict):
    history: List[dict]
    context: List[str]
    answer: str

# Retrieve context from Pinecone


def retrieve(state: State) -> dict:
    current_question = None
    for msg in reversed(state["history"]):
        if msg.get("role") == "user":
            current_question = msg.get("content")
            break
    if not current_question:
        current_question = state["history"][-1].get("content", "")

    # Choose correct embedding interface
    if env == "development":
        query_embedding = embeddings.embed_query(current_question)
    else:
        query_embedding = embeddings.embed_query(current_question)

    result = pinecone_index.query(
        vector=query_embedding,
        top_k=10,
        namespace="docs",
        include_metadata=True,
    )
    context = ""
    for match in result.get("matches", []):
        metadata = match.get("metadata", {})
        text = metadata.get("text", "")
        if text:
            context += text + "\n\n"
    return {"context": [context.strip()]}

# Generate an answer using Gemini


def generate(state: State) -> dict:
    messages = [get_system_message()]
    for msg in state["history"]:
        role = msg.get("role")
        content = msg.get("content")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
        elif role == "system":
            messages.append(SystemMessage(content=content))

    if state["context"] and state["context"][0]:
        context_message = HumanMessage(
            content=f"Relevant context:\n{state['context'][0]}")
        messages.append(context_message)

    gemini_model = get_gemini_model()
    response = gemini_model.invoke(messages)
    return {"answer": response.content}


# LangGraph structure
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

router = APIRouter()


@router.post("/chat")
async def chat(query: QueryHistory):
    try:
        async def token_generator():
            state_input = {"history": [msg.dict() for msg in query.history]}
            async for chunk in graph.astream(state_input, stream_mode="messages"):
                yield chunk[0].content
        return StreamingResponse(token_generator(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggest-followups")
async def suggest_followups(query: QueryHistory):
    try:
        gemini_model = get_gemini_model()
        messages = [get_system_message()]
        for msg in query.history:
            role = msg.role
            content = msg.content
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))
            elif role == "system":
                messages.append(SystemMessage(content=content))
        messages.append(HumanMessage(
            content="Suggest 1 or 2 very short follow-up questions (3 to 5 words max each). Be concise and respond only in text without markdown."))
        response = gemini_model.invoke(messages)
        suggestions = response.content.strip().split("\n")
        cleaned = [s.lstrip("1234567890.-) ").strip()
                   for s in suggestions if s.strip()]
        return {"suggestions": cleaned}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
