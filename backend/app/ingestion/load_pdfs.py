import os
import time
import requests
import tempfile
import urllib.parse
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings

# Initialize Pinecone
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Initialize HuggingFace Embeddings using an open source model
embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

def download_pdf(url):
    # Handle file:// URLs
    if url.startswith("file://"):
        parsed = urllib.parse.urlparse(url)
        local_path = urllib.parse.unquote(parsed.path)
        if os.name == 'nt' and local_path.startswith('/'):
            local_path = local_path.lstrip('/')
        if not os.path.exists(local_path):
            raise Exception(f"Local file not found: {local_path}")
        return local_path
    # Handle plain local file paths (Windows or Unix)
    elif os.path.isabs(url) and os.path.exists(url):
        return url
    # Otherwise, treat as remote URL
    else:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Failed to download PDF from {url}. Status code: {response.status_code}"
            )
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file.write(response.content)
        temp_file.close()
        return temp_file.name

def extract_documents_from_pdf(pdf_path, source_url):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Add the source URL to metadata for each document
    for doc in documents:
        doc.metadata["source"] = source_url

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_documents(documents)

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

    # Get text chunks
    texts = [chunk.page_content for chunk in chunks]

    print("Embedding text chunks using HuggingFace Embeddings...")
    try:
        # Generate embeddings for all text chunks at once
        document_embeddings = embeddings.embed_documents(texts)
    except Exception as e:
        print(f"Embedding failed: {e}")
        document_embeddings = [[0.0] * settings.EMBEDDING_DIMENSION for _ in texts]

    # Format vectors for Pinecone
    vectors = [
        {
            "id": f"doc-{i}",
            "values": embedding,
            "metadata": {
                "text": text,
                "source": chunks[i].metadata.get("source", "unknown")
            }
        }
        for i, (text, embedding) in enumerate(zip(texts, document_embeddings))
    ]

    print(
        f"Upserting {len(vectors)} vectors into Pinecone (namespace='docs')...")
    index.upsert(vectors=vectors, namespace="docs")
    print("Upload complete!")

def main():
    all_chunks = []
    for url in settings.FILES:
        print(f"Processing file from: {url}")
        try:
            pdf_path = download_pdf(url)
            chunks = extract_documents_from_pdf(pdf_path, source_url=url)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"Error processing {url}: {e}")

    if all_chunks:
        embed_and_upload_to_pinecone(all_chunks)
    else:
        print("No chunks to upload.")

if __name__ == "__main__":
    main()
