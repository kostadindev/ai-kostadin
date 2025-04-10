from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from pinecone import Pinecone
from typing_extensions import TypedDict, List
from pydantic import BaseModel

from langgraph.graph import START, StateGraph

load_dotenv()


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


# Initialize Pinecone, embeddings, and Gemini model.
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_region = os.getenv("PINECONE_API_REGION", "us-east-1")
pinecone_index_name = os.getenv("PINECONE_API_INDEX", "document-index")
pc = Pinecone(api_key=pinecone_api_key)
pinecone_index = pc.Index(pinecone_index_name)

embeddings = HuggingFaceInferenceEmbeddings()

SYSTEM_PROMPT = (
    "You are AI Kostadin and you are a chatbot for Kostadin's personal website. "
    "Answer questions about him and his work. Do not answer unrelated or inappropriate questions. "
    "If context is provided, use it to inform your answer."
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
    role: str  # Expected values: "system", "user", "assistant"
    content: str


class QueryHistory(BaseModel):
    history: List[ChatMessage]


# Update the LangGraph state to include a conversation history list.
class State(TypedDict):
    history: List[dict]  # each dict should have a role and content field
    context: List[str]
    answer: str


# Retrieve function: get the current question from the last user message.
def retrieve(state: State) -> dict:
    current_question = None
    # Find the most recent user message.
    for msg in reversed(state["history"]):
        if msg.get("role") == "user":
            current_question = msg.get("content")
            break
    if not current_question:
        current_question = state["history"][-1].get("content", "")
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


# Generation function: build a list of messages using the multi-turn structure.
def generate(state: State) -> dict:
    messages = [get_system_message()]
    # Convert each chat message in the history to the proper LangChain message type.
    for msg in state["history"]:
        role = msg.get("role")
        content = msg.get("content")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
        elif role == "system":
            messages.append(SystemMessage(content=content))
    # Optionally, add the retrieved context as a separate message.
    if state["context"] and state["context"][0]:
        context_message = HumanMessage(
            content=f"Relevant context:\n{state['context'][0]}")
        messages.append(context_message)

    gemini_model = get_gemini_model()
    response = gemini_model.invoke(messages)
    return {"answer": response.content}


# Build the LangGraph state graph.
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

router = APIRouter()


@router.post("/chat")
async def chat(query: QueryHistory):
    """
    Updated endpoint to accept a conversation history with multiple turns.
    Each message includes a role ("system", "user", or "assistant") and content.
    """
    try:
        async def token_generator():
            # Convert the pydantic objects to dicts for the internal state.
            state_input = {"history": [msg.dict() for msg in query.history]}
            async for chunk in graph.astream(state_input, stream_mode="messages"):
                yield chunk[0].content

        return StreamingResponse(token_generator(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggest-followups")
async def suggest_followups(query: QueryHistory):
    """
    Suggest follow-up questions based on the current conversation history.
    """
    try:
        gemini_model = get_gemini_model()

        # Build the prompt to ask for follow-up suggestions
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
            content="Based on the above, suggest 3 thoughtful follow-up questions a user might ask next."))

        response = gemini_model.invoke(messages)
        suggestions = response.content.strip().split("\n")

        # Normalize suggestions (remove any leading numbering or dashes)
        cleaned = [s.lstrip("1234567890.-) ").strip()
                   for s in suggestions if s.strip()]
        return {"suggestions": cleaned}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
