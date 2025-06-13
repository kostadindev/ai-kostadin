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
            try:
                async for chunk in graph.astream(state_input, stream_mode="messages"):
                    yield chunk[0].content
            except Exception as stream_exc:
                raise
        response = StreamingResponse(token_generator(), media_type="text/plain")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggest-followups")
async def suggest_followups(query: QueryHistory):
    """
    Generate follow-up question suggestions focused on technical terms, unique terminology, 
    and unique aspects about Kostadin, avoiding previously asked questions.
    
    Args:
        query: The chat history.
        
    Returns:
        Dictionary containing suggested follow-up questions, or empty list if no good follow-ups.
    """
    try:
        # Extract previous questions to avoid repetition
        previous_questions = [
            msg.content.lower().strip() 
            for msg in query.history 
            if msg.role == "user"
        ]
        
        messages = gemini_service.create_messages(
            [msg.dict() for msg in query.history]
        )
        messages.append(HumanMessage(
            content="Based on the conversation, suggest 1-2 NEW follow-up questions on the previous answerthat either: "
            "1) Ask for clarification about technical terms, key concepts, or unique terminology mentioned, or "
            "2) Explore unique aspects about Kostadin's background, experience, or preferences. "
            "Look for domain-specific terms, acronyms, or specialized vocabulary that might need explanation. "
            "IMPORTANT: Do not suggest questions that have already been asked in the conversation. "
            "Keep questions under 5 words each. If there are no new technical terms, unique terminology, or "
            "unique aspects to explore, respond with 'NO_FOLLOWUP'. Answer in a simple string. "
            "Be specific and avoid generic questions."
        ))
        response = gemini_service.generate_response(messages)
        
        if "NO_FOLLOWUP" in response.upper():
            return {"suggestions": []}
            
        suggestions = [s.strip() for s in response.strip().split("\n") if s.strip()][:2]
        cleaned = [s.lstrip("1234567890.-) ").strip() for s in suggestions if s.strip()]
        
        # Filter out suggestions that are too similar to previous questions
        filtered_suggestions = []
        for suggestion in cleaned:
            suggestion_lower = suggestion.lower()
            # Check if this suggestion is too similar to any previous question
            if not any(
                suggestion_lower in prev_q or prev_q in suggestion_lower 
                for prev_q in previous_questions
            ):
                filtered_suggestions.append(suggestion)
        
        return {"suggestions": filtered_suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
