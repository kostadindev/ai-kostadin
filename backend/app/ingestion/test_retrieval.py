# test_retrieval.py
import os
import math
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings


def main():
    # === Load environment variables ===
    load_dotenv()
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_region = os.getenv("PINECONE_REGION", "us-east-1")
    pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "document-index")

    # === Initialize Pinecone ===
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(pinecone_index_name)

    # === Initialize HuggingFace Embeddings ===
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # === Hardcoded queries ===
    queries = [
        "What information does the GitHub repository provide?",
        "Summarize the contents of the PDF document.",
        "Describe the website content processed from the sitemap.",
        "How does the embedding process work for text documents?",
        "Explain the steps involved in creating a vector database."
    ]

    # Process each query
    for query_text in queries:
        print(f"\nQuery: {query_text}")
        query_embedding = embeddings.embed_query(query_text)
        # Ensure every element is a standard Python float and is finite.
        query_vector = [float(val) if math.isfinite(
            val) else 0.0 for val in query_embedding]

        # Query the Pinecone index for top 5 matches
        result = index.query(
            vector=query_embedding, top_k=5, namespace="docs", include_metadata=True)
        matches = result.get("matches", [])
        if not matches:
            print("No matches found.")
        else:
            for match in matches:
                print(f"\nID: {match.get('id', 'N/A')}")
                print(f"Score: {match.get('score', 'N/A')}")
                print(f"Metadata: {match.get('metadata', {})}")
        print("\n" + "-" * 50)


if __name__ == "__main__":
    main()
