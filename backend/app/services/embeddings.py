"""
Embeddings service for handling text embeddings using HuggingFace.
"""
from typing import List, Union
from huggingface_hub import InferenceClient
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings

class EmbeddingsService:
    """Service for handling text embeddings."""
    
    def __init__(self):
        """Initialize the embeddings service based on environment."""
        if settings.ENV == "production":
            self._client = InferenceClient(token=settings.HF_API_TOKEN)
            self._model = settings.EMBEDDING_MODEL
        else:
            self._embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL
            )
    
    def embed_query(self, text: str) -> List[float]:
        """
        Generate embeddings for the given text.
        
        Args:
            text: The text to generate embeddings for.
            
        Returns:
            List of float values representing the embedding.
        """
        if settings.ENV == "production":
            embedding = self._client.feature_extraction(text, model=self._model)
            return embedding.tolist() if hasattr(embedding, "tolist") else embedding
        else:
            return self._embeddings.embed_query(text)

# Create a global embeddings service instance
embeddings_service = EmbeddingsService() 