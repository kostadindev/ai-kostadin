"""
Pinecone service for handling vector database operations.
"""
from typing import List, Dict, Any
from pinecone import Pinecone
from app.config import settings

class PineconeService:
    """Service for handling Pinecone vector database operations."""
    
    def __init__(self):
        """Initialize the Pinecone service."""
        self._pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self._index = self._pc.Index(settings.PINECONE_API_INDEX)
    
    def query(self, vector: List[float], top_k: int = 5, namespace: str = "docs") -> Dict[str, Any]:
        """
        Query the Pinecone index for similar vectors.
        
        Args:
            vector: The query vector to search for.
            top_k: Number of results to return.
            namespace: The namespace to search in.
            
        Returns:
            Dictionary containing the query results.
        """
        return self._index.query(
            vector=vector,
            top_k=top_k,
            namespace=namespace,
            include_metadata=True
        )
    
    def get_context(self, query_result: Dict[str, Any]) -> str:
        """
        Extract context from Pinecone query results.
        
        Args:
            query_result: The result from a Pinecone query.
            
        Returns:
            Concatenated context string from the results.
        """
        context = ""
        for match in query_result.get("matches", []):
            metadata = match.get("metadata", {})
            text = metadata.get("text", "")
            if text:
                context += text + "\n\n"
        return context.strip()

# Create a global Pinecone service instance
pinecone_service = PineconeService() 