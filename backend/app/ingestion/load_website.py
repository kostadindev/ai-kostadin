import os
import time
import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings

# Initialize Pinecone
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Initialize HuggingFace Embeddings using an open source model
embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

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
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_documents([document])

def embed_and_upload_to_pinecone(chunks):
    # Check if the index exists; if not, create it.
    if settings.PINECONE_API_INDEX not in pc.list_indexes().names():
        print(f"Creating index: {settings.PINECONE_API_INDEX}")
        pc.create_index(
            name=settings.PINECONE_API_INDEX,
            dimension=settings.EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=settings.PINECONE_API_REGION)
        )
        # Wait until index is ready
        while not pc.describe_index(settings.PINECONE_API_INDEX).status['ready']:
            time.sleep(1)
    else:
        print(f"Index {settings.PINECONE_API_INDEX} already exists.")

    index = pc.Index(settings.PINECONE_API_INDEX)

    texts = [chunk.page_content for chunk in chunks]
    print("Embedding HTML text chunks using HuggingFace Embeddings...")

    try:
        # Embed all text chunks at once
        document_embeddings = embeddings.embed_documents(texts)
    except Exception as e:
        print(f"Embedding failed: {e}")
        document_embeddings = [[0.0] * settings.EMBEDDING_DIMENSION for _ in texts]

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
    print(f"Fetching sitemap: {settings.SITEMAP_URL}")
    try:
        urls = get_urls_from_sitemap(settings.SITEMAP_URL)
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
