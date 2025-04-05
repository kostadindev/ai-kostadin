import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables from .env file
load_dotenv()

# Environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_region = os.getenv("PINECONE_REGION", "us-east-1")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "document-index")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)

# Initialize HuggingFace Embeddings using an open source model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

SITEMAP_URL = "https://kostadindev.github.io/sitemap.xml"


def get_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        raise Exception(f"Failed to load sitemap: {response.status_code}")
    soup = BeautifulSoup(response.text, "xml")
    return [loc.text for loc in soup.find_all("loc")]


def download_and_clean_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download HTML: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


def split_into_chunks(text, source_url):
    document = Document(page_content=text, metadata={"source": source_url})
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_documents([document])


def embed_and_upload_to_pinecone(chunks):
    # Delete the existing index if it exists
    if pinecone_index_name in pc.list_indexes().names():
        print(f"Deleting index: {pinecone_index_name}")
        pc.delete_index(pinecone_index_name)

    # Create a new index
    print(f"Creating index: {pinecone_index_name}")
    # For "all-MiniLM-L6-v2", the embedding dimension is 384.
    pc.create_index(
        name=pinecone_index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=pinecone_region)
    )

    # Wait until the index is ready
    while not pc.describe_index(pinecone_index_name).status['ready']:
        time.sleep(1)

    index = pc.Index(pinecone_index_name)

    texts = [chunk.page_content for chunk in chunks]
    print("Embedding HTML text chunks using HuggingFace Embeddings...")

    try:
        # Embed all text chunks at once
        document_embeddings = embeddings.embed_documents(texts)
    except Exception as e:
        print(f"Embedding failed: {e}")
        document_embeddings = [[0.0] * 384 for _ in texts]

    vectors = [
        {
            "id": f"html-{i}",
            "values": embedding,
            "metadata": {
                "text": text,
                "source": chunks[i].metadata.get("source", "unknown")
            }
        }
        for i, (text, embedding) in enumerate(zip(texts, document_embeddings))
    ]

    print(f"Upserting {len(vectors)} vectors into Pinecone...")
    index.upsert(vectors=vectors, namespace="docs")
    print("✅ Upload complete!")


def main():
    print(f"Fetching sitemap: {SITEMAP_URL}")
    try:
        urls = get_urls_from_sitemap(SITEMAP_URL)
        all_chunks = []

        for url in urls:
            print(f"Processing: {url}")
            try:
                text = download_and_clean_html(url)
                chunks = split_into_chunks(text, source_url=url)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"❌ Error for {url}: {e}")

        print(f"\n✅ Total Chunks Prepared: {len(all_chunks)}")
        embed_and_upload_to_pinecone(all_chunks)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
