"""
Configuration management for the application.
Centralizes all environment variables and settings in one place.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Environment
    ENV: str = os.getenv("ENV", "development")
    
    # API Keys
    GOOGLE_API_KEY: str
    HF_API_TOKEN: str
    PINECONE_API_KEY: str
    GITHUB_API_KEY: Optional[str] = None
    
    # Pinecone Configuration
    PINECONE_API_REGION: str = os.getenv("PINECONE_API_REGION", "us-east-1")
    PINECONE_API_INDEX: str = os.getenv("PINECONE_API_INDEX", "document-index")
    
    # Model Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_TEMPERATURE: float = 0.7
    
    # System Prompt
    SYSTEM_PROMPT: str = (
        "You are AI Kostadin and you are a chatbot for Kostadin's personal website. "
        "Answer questions about him and his work. Do not answer unrelated or inappropriate questions. "
        "If context is provided and immediately relevant to the question, use it to inform your answer."
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields in the environment

# Create a global settings instance
settings = Settings() 