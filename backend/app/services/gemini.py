"""
Gemini service for handling LLM operations.
"""
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from app.config import settings

class GeminiService:
    """Service for handling Gemini LLM operations."""
    
    def __init__(self):
        """Initialize the Gemini service."""
        self._model = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            temperature=settings.GEMINI_TEMPERATURE,
            api_key=settings.GOOGLE_API_KEY
        )
        self._system_message = SystemMessage(content=settings.SYSTEM_PROMPT)
    
    def get_system_message(self) -> SystemMessage:
        """Get the system message for the chat."""
        return self._system_message
    
    def create_messages(self, history: List[dict], context: str = "") -> List[SystemMessage | HumanMessage | AIMessage]:
        """
        Create a list of messages for the LLM from chat history and context.
        
        Args:
            history: List of chat messages.
            context: Optional context to include in the messages.
            
        Returns:
            List of formatted messages for the LLM.
        """
        messages = [self._system_message]
        
        for msg in history:
            role = msg.get("role")
            content = msg.get("content")
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))
            elif role == "system":
                messages.append(SystemMessage(content=content))
        
        if context:
            messages.append(HumanMessage(content=f"Relevant context:\n{context}"))
        
        return messages
    
    def generate_response(self, messages: List[SystemMessage | HumanMessage | AIMessage]) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            messages: List of messages to send to the LLM.
            
        Returns:
            The generated response text.
        """
        response = self._model.invoke(messages)
        return response.content

# Create a global Gemini service instance
gemini_service = GeminiService() 