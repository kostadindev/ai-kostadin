from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from typing_extensions import TypedDict, List

from langgraph.graph import START, StateGraph
from app.models.query import Query

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
        return embedding.tolist() if hasattr(embedding, 'tolist') else embedding


# Initialize Pinecone, embeddings, and Gemini model.
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_region = os.getenv("PINECONE_REGION", "us-east-1")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "document-index")
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
        api_key=api_key
    )


def get_system_message():
    return SystemMessage(content=SYSTEM_PROMPT)


# Define the state for LangGraph.
class State(TypedDict):
    question: str
    context: List[str]
    answer: str


# Define the retrieval step: embed the question and query Pinecone.
def retrieve(state: State) -> dict:
    query_embedding = embeddings.embed_query(state["question"])
    result = pinecone_index.query(
        vector=query_embedding,
        top_k=10,
        namespace="docs",
        include_metadata=True
    )
    matches = result.get("matches", [])
    context = ""
    for match in matches:
        metadata = match.get("metadata", {})
        text = metadata.get("text", "")
        if text:
            context += text + "\n\n"
    return {"context": [context.strip()]}


# Define the generation step: build the augmented question and get the answer.
def generate(state: State) -> dict:
    # Build the prompt with context if available.
    if state["context"] and state["context"][0]:
        augmented_question = f"Context:\n{state['context'][0]}\nQuestion: {state['question']}"
    else:
        augmented_question = state["question"]

    system_message = get_system_message()
    user_message = HumanMessage(content=augmented_question)

    # Get the answer synchronously.
    gemini_model = get_gemini_model()
    response = gemini_model.invoke([system_message, user_message])
    return {"answer": response.content}


# Build the LangGraph state graph.
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

router = APIRouter()


@router.post("/chat")
async def chat(query: Query):
    try:
        async def token_generator():
            # Use astream() with mode "messages" to yield tokens as they are produced.
            async for chunk in graph.astream({"question": query.question}, stream_mode="messages"):
                # Each chunk is expected to be an object with a 'content' attribute.
                yield chunk[0].content
        return StreamingResponse(token_generator(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
