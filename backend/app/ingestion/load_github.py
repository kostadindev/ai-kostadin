import os
import time
import requests
import tempfile
import hashlib
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings

# === Load environment variables ===
load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_region = os.getenv("PINECONE_REGION", "us-east-1")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "document-index")
github_token = os.getenv("GITHUB_API_KEY")
github_username = os.getenv("GITHUB_USERNAME", "kostadindev")

headers = {"Authorization": f"token {github_token}"} if github_token else {}

# === Initialize Pinecone ===
pc = Pinecone(api_key=pinecone_api_key)

# Optional: create the index if it doesn't exist (for "all-MiniLM-L6-v2", dimension is 384)
if pinecone_index_name not in pc.list_indexes().names():
    print(f"Creating index: {pinecone_index_name}")
    pc.create_index(
        name=pinecone_index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=pinecone_region)
    )
# Get the index
index = pc.Index(pinecone_index_name)

# === Initialize HuggingFace Embeddings ===
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def get_user_repos():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{github_username}/repos?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"GitHub API error: {response.status_code} - {response.text}")
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return [repo['name'] for repo in repos]


def get_repo_files(repo):
    def fetch_files_recursively(path=""):
        url = f"https://api.github.com/repos/{github_username}/{repo}/contents/{path}"
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
    repos = get_user_repos()
    all_md_urls = []
    for repo in repos:
        print(f"🔍 Scanning repo: {repo}")
        md_files = get_repo_files(repo)
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
        chunk_size=300,
        chunk_overlap=50,
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
        document_embeddings = [[0.0] * 384 for _ in texts]

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
