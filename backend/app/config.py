"""
Configuration management for the application.
Centralizes all environment variables and settings in one place.
"""
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings and configuration."""

    # Environment
    ENV: str = Field(default="development", description="Environment type (development, production, etc.)")
    
    # API Keys
    GOOGLE_API_KEY: str = Field(..., description="Google API Key")
    HF_API_TOKEN: str = Field(..., description="Hugging Face API Token")
    PINECONE_API_KEY: str = Field(..., description="Pinecone API Key")
    GITHUB_API_KEY: Optional[str] = Field(default=None, description="Optional GitHub API Key")
    
    # Pinecone Configuration
    PINECONE_API_REGION: str = Field(default="us-east-1", description="Pinecone region")
    PINECONE_API_INDEX: str = Field(default="document-index", description="Pinecone index name")
    
    # Model Configuration
    # 🔄 Changed to model that is actually available on Hugging Face's inference API
    EMBEDDING_MODEL: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", description="Embedding model used for feature extraction")
    GEMINI_MODEL: str = Field(default="gemini-2.0-flash", description="Gemini model to use")
    GEMINI_TEMPERATURE: float = Field(default=0.7, ge=0.0, le=1.0, description="Temperature for Gemini model")
    
    # System Prompt
    SYSTEM_PROMPT: str = Field(
        default=(
            "You are AI Kostadin and you are a chatbot for Kostadin's personal website. "
            "Answer questions about him and his work. Do not answer unrelated or inappropriate questions. "
            "If context is provided and immediately relevant to the question, use it to inform your answer."
        ),
        description="Default system prompt for AI assistant"
    )

    # Ingestion Configuration
    FILES: List[str] = Field(
        default=[
            # PDF documents - remote
            "https://kostadindev.github.io/static/documents/cv.pdf",
            "https://kostadindev.github.io/static/documents/sbu_transcript.pdf",
            "https://kostadindev.github.io/static/documents/uhh_transcript.pdf",
            "C:/Users/kosta/OneDrive/Desktop/MS Application Materials/emf-ellipse-publication.pdf",
        ],
        description="List of files to process (remote URLs or local file paths)"
    )
    SITEMAP_URL: str = Field(default="https://kostadindev.github.io/sitemap.xml", description="URL of the sitemap to crawl")
    GITHUB_REPOSITORIES: List[str] = Field(
        default=[
            "https://github.com/kostadindev/Knowledge-Base-Builder",
            "https://github.com/kostadindev/GONEXT",
            "https://github.com/kostadindev/GONEXT-ML",
            "https://github.com/kostadindev/ai-kostadin",
            "https://github.com/kostadindev/Recursive-QA",
            "https://github.com/kostadindev/deep-gestures",
            "https://github.com/kostadindev/emf-ellipse"
        ],
        description="List of GitHub repositories to process (format: username/repo or full URL)"
    )
    
    # Text Processing Configuration
    CHUNK_SIZE: int = Field(default=600, description="Size of text chunks for splitting documents")
    CHUNK_OVERLAP: int = Field(default=50, description="Overlap between text chunks")
    EMBEDDING_DIMENSION: int = Field(default=384, description="Dimension of embeddings (for all-MiniLM-L6-v2)")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields in the environment

# Global settings instance
settings = Settings()
