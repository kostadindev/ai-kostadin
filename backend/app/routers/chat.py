"""
Chat router for handling chat-related endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict
from langchain.schema import HumanMessage

from app.services.embeddings import embeddings_service
from app.services.pinecone import pinecone_service
from app.services.gemini import gemini_service

# Define models for conversation history
class ChatMessage(BaseModel):
    """Model for a single chat message."""
    role: str  # "system", "user", or "assistant"
    content: str

class QueryHistory(BaseModel):
    """Model for chat history."""
    history: List[ChatMessage]

# LangGraph state
class State(TypedDict):
    """State for the LangGraph workflow."""
    history: List[dict]
    context: List[str]
    answer: str

def retrieve(state: State) -> dict:
    """
    Retrieve relevant context from Pinecone based on the current question.
    
    Args:
        state: Current state of the conversation.
        
    Returns:
        Dictionary containing the retrieved context.
    """
    # Get the current question from the history
    current_question = None
    for msg in reversed(state["history"]):
        if msg.get("role") == "user":
            current_question = msg.get("content")
            break
    if not current_question:
        current_question = state["history"][-1].get("content", "")

    # Generate embeddings and query Pinecone
    query_embedding = embeddings_service.embed_query(current_question)
    query_result = pinecone_service.query(vector=query_embedding)
    context = pinecone_service.get_context(query_result)
    
    return {"context": [context]}

def generate(state: State) -> dict:
    """
    Generate a response using the Gemini model.
    
    Args:
        state: Current state of the conversation.
        
    Returns:
        Dictionary containing the generated answer.
    """
    context = state["context"][0] if state["context"] else ""
    messages = gemini_service.create_messages(state["history"], context)
    answer = gemini_service.generate_response(messages)
    return {"answer": answer}

# Set up the LangGraph workflow
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

router = APIRouter()

@router.post("/chat")
async def chat(query: QueryHistory):
    """
    Handle chat requests and stream responses.
    
    Args:
        query: The chat history and current query.
        
    Returns:
        StreamingResponse with the generated response.
    """
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
    """
    Generate follow-up question suggestions.
    
    Args:
        query: The chat history.
        
    Returns:
        Dictionary containing suggested follow-up questions.
    """
    try:
        messages = gemini_service.create_messages(
            [msg.dict() for msg in query.history]
        )
        messages.append(HumanMessage(
            content="Suggest 1 or 2 very short follow-up questions (3 to 5 words max each). "
            "Be concise and respond only in text without markdown."
        ))
        response = gemini_service.generate_response(messages)
        suggestions = response.strip().split("\n")
        cleaned = [s.lstrip("1234567890.-) ").strip() for s in suggestions if s.strip()]
        return {"suggestions": cleaned}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
