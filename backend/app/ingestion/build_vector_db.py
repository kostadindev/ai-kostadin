# build_vector_db.py
import os
import time
from pinecone import Pinecone, ServerlessSpec

# Import the main functions from your three ingestion scripts.
# Each script should be refactored to accept an 'index' parameter.
from .load_github import main as load_github_main
from .load_pdfs import main as load_pdfs_main
from .load_website import main as load_website_main
from ..config import settings

def main():
    # === Initialize Pinecone ===
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    # === Delete the existing index if it exists ===
    if settings.PINECONE_API_INDEX in pc.list_indexes().names():
        print(f"Deleting existing index: {settings.PINECONE_API_INDEX}")
        pc.delete_index(settings.PINECONE_API_INDEX)
        # Allow some time for deletion to propagate.
        time.sleep(3)

    # === Create a new index here ===
    print(f"Creating new index: {settings.PINECONE_API_INDEX}")
    pc.create_index(
        name=settings.PINECONE_API_INDEX,
        dimension=settings.EMBEDDING_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=settings.PINECONE_API_REGION)
    )
    # Optionally wait until the index is ready.
    while not pc.describe_index(settings.PINECONE_API_INDEX).status.get("ready", False):
        print("Waiting for index to be ready...")
        time.sleep(1)
    index = pc.Index(settings.PINECONE_API_INDEX)
    print("Index is ready.")

    # === Call the ingestion scripts using the new index ===
    print("\n--- Running GitHub Loader ---")
    load_github_main()

    print("\n--- Running PDF Loader ---")
    load_pdfs_main()

    print("\n--- Running Website Loader ---")
    load_website_main()

    print("\nAll data has been ingested into the new Pinecone index!")

if __name__ == "__main__":
    main()
