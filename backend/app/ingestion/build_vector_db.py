# build_vector_db.py
import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Import the main functions from your three ingestion scripts.
# Each script should be refactored to accept an 'index' parameter.
from load_github import main as load_github_main
from load_pdfs import main as load_pdfs_main
from load_website import main as load_website_main


def main():
    # === 1. Load environment variables ===
    load_dotenv()

    # === 2. Pinecone configuration ===
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_region = os.getenv("PINECONE_REGION", "us-east-1")
    pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "document-index")
    embedding_dim = 384  # For "all-MiniLM-L6-v2"

    # === 3. Initialize Pinecone ===
    pc = Pinecone(api_key=pinecone_api_key)

    # === 4. Delete the existing index if it exists ===
    if pinecone_index_name in pc.list_indexes().names():
        print(f"Deleting existing index: {pinecone_index_name}")
        pc.delete_index(pinecone_index_name)
        # Allow some time for deletion to propagate.
        time.sleep(3)

    # === 5. Create a new index here ===
    print(f"Creating new index: {pinecone_index_name}")
    pc.create_index(
        name=pinecone_index_name,
        dimension=embedding_dim,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=pinecone_region)
    )
    # Optionally wait until the index is ready.
    while not pc.describe_index(pinecone_index_name).status.get("ready", False):
        print("Waiting for index to be ready...")
        time.sleep(1)
    index = pc.Index(pinecone_index_name)
    print("Index is ready.")

    # === 6. Call the ingestion scripts using the new index ===
    print("\n--- Running GitHub Loader ---")
    load_github_main()

    print("\n--- Running PDF Loader ---")
    load_pdfs_main()

    print("\n--- Running Website Loader ---")
    load_website_main()

    print("\nAll data has been ingested into the new Pinecone index!")


if __name__ == "__main__":
    main()
