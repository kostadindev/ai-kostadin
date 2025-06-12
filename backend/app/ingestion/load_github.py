import os
import time
import requests
import tempfile
import hashlib
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings

# Initialize Pinecone
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Initialize HuggingFace Embeddings
embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

headers = {"Authorization": f"token {settings.GITHUB_API_KEY}"} if settings.GITHUB_API_KEY else {}

def get_repo_files(repo_url):
    # Extract username and repo from the URL
    parts = repo_url.strip('/').split('/')
    if len(parts) < 2:
        raise ValueError(f"Invalid GitHub URL: {repo_url}")
    username, repo = parts[-2], parts[-1]
    
    def fetch_files_recursively(path=""):
        url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return []
        contents = response.json()
        files = []
        for item in contents:
            if item['type'] == 'file' and item['name'].endswith('.md'):
                files.append(item['download_url'])
            elif item['type'] == 'dir':
                files.extend(fetch_files_recursively(item['path']))
        return files
    return fetch_files_recursively()

def get_all_markdown_urls():
    all_md_urls = []
    for repo_url in settings.GITHUB_REPOSITORIES:
        print(f"🔍 Scanning repo: {repo_url}")
        md_files = get_repo_files(repo_url)
        all_md_urls.extend(md_files)
    return all_md_urls

def download_markdown(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to download Markdown file. Status code: {response.status_code}")
    temp_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=".md", mode='w', encoding='utf-8')
    temp_file.write(response.text)
    temp_file.close()
    return temp_file.name

def extract_documents_from_markdown(md_path, source_url):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    doc = Document(page_content=content, metadata={"source": source_url})

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    return splitter.split_documents([doc])

def embed_and_upload_to_pinecone(chunks):
    if not chunks:
        print("⚠️ No chunks to embed.")
        return

    print(f"\n🧠 Preparing {len(chunks)} chunks for HuggingFace embedding...")

    texts = []
    for i, chunk in enumerate(chunks):
        content = chunk.page_content
        print(f"\n--- Chunk {i + 1} ---")
        print(f"📄 Source: {chunk.metadata.get('source', 'unknown')}")
        print(f"🔢 Characters: {len(content)}")
        print(f"📝 Content:\n{content}\n")
        texts.append(content)

    print(f"\n🔢 Total Chunks Ready: {len(texts)}")

    try:
        # Embed all text chunks at once using the open source model
        document_embeddings = embeddings.embed_documents(texts)
    except Exception as e:
        print(f"❌ HuggingFace embedding failed: {e}")
        document_embeddings = [[0.0] * settings.EMBEDDING_DIMENSION for _ in texts]

    vectors = []
    for i, (chunk, embedding) in enumerate(zip(chunks, document_embeddings)):
        hash_id = hashlib.md5(chunk.page_content.encode()).hexdigest()
        vectors.append({
            "id": f"github-{hash_id}",
            "values": embedding,
            "metadata": {
                "text": chunk.page_content,
                "source": chunk.metadata.get("source", "unknown")
            }
        })

    print(
        f"\n📤 Upserting {len(vectors)} vectors into Pinecone (namespace='docs')...")
    index = pc.Index(settings.PINECONE_API_INDEX)
    index.upsert(vectors=vectors, namespace="docs")
    print("✅ Upload complete!")

def main():
    print("📡 Fetching markdown URLs from GitHub...")
    markdown_urls = get_all_markdown_urls()

    print(f"\n📄 Found {len(markdown_urls)} Markdown files.")
    all_chunks = []

    for url in markdown_urls:
        print(f"\n➡️ Processing: {url}")
        try:
            md_path = download_markdown(url)
            chunks = extract_documents_from_markdown(md_path, source_url=url)
            all_chunks.extend(chunks)
            os.unlink(md_path)
        except Exception as e:
            print(f"❌ Error processing {url}: {e}")

    print(f"\n🧩 Total Chunks Created: {len(all_chunks)}")
    embed_and_upload_to_pinecone(all_chunks)

if __name__ == "__main__":
    main()
