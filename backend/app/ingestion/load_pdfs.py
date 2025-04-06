import os
import time
import requests
import tempfile
import urllib.parse
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

# Environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_region = os.getenv("PINECONE_REGION", "us-east-1")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "document-index")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)

# Initialize HuggingFace Embeddings using an open source model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def download_pdf(url):
    if url.startswith("file://"):
        # Parse the file URL to get the local file path and decode percent-encoded characters
        parsed = urllib.parse.urlparse(url)
        local_path = urllib.parse.unquote(parsed.path)
        # On Windows, remove the leading slash if present (e.g., /C:/...)
        if os.name == 'nt' and local_path.startswith('/'):
            local_path = local_path.lstrip('/')
        if not os.path.exists(local_path):
            raise Exception(f"Local file not found: {local_path}")
        return local_path
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
        chunk_size=600,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_documents(documents)


def embed_and_upload_to_pinecone(chunks):
    # Check if the index exists; if not, create it.
    if pinecone_index_name not in pc.list_indexes().names():
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
    else:
        print(f"Index {pinecone_index_name} already exists.")

    index = pc.Index(pinecone_index_name)

    # Get text chunks
    texts = [chunk.page_content for chunk in chunks]

    print("Embedding text chunks using HuggingFace Embeddings...")
    try:
        # Generate embeddings for all text chunks at once
        document_embeddings = embeddings.embed_documents(texts)
    except Exception as e:
        print(f"Embedding failed: {e}")
        document_embeddings = [[0.0] * 384 for _ in texts]

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
    # List of PDF URLs to process, including a remote and a local URL.
    pdf_urls = [
        "https://kostadindev.github.io/static/documents/cv.pdf",
        "https://kostadindev.github.io/static/documents/sbu_transcript.pdf",
        "file:///C:/Users/kosta/OneDrive/Desktop/MS%20Application%20Materials/emf-ellipse-publication.pdf"
    ]

    all_chunks = []
    for url in pdf_urls:
        print(f"Processing PDF from: {url}")
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
