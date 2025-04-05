import requests
import tempfile
import os
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

GITHUB_API = "https://api.github.com"
USERNAME = "kostadindev"

# === GITHUB SCRAPER ===


def get_user_repos():
    """Fetch public repositories for kostadindev."""
    repos = []
    page = 1
    while True:
        url = f"{GITHUB_API}/users/{USERNAME}/repos?per_page=100&page={page}"
        response = requests.get(url)
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return [repo['name'] for repo in repos]


def get_repo_files(repo):
    """Recursively get all .md files from a GitHub repo."""
    def fetch_files_recursively(path=""):
        url = f"{GITHUB_API}/repos/{USERNAME}/{repo}/contents/{path}"
        response = requests.get(url)
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
    """Extract Markdown file URLs from all public repos of kostadindev."""
    repos = get_user_repos()
    all_md_urls = []
    for repo in repos:
        print(f"Scanning repo: {repo}")
        md_files = get_repo_files(repo)
        all_md_urls.extend(md_files)
    return all_md_urls

# === DOCUMENT LOADING ===


def download_markdown(url):
    """Download a markdown file and return its local path."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to download Markdown file. Status code: {response.status_code}")

    temp_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=".md", mode='w', encoding='utf-8')
    temp_file.write(response.text)
    temp_file.close()
    return temp_file.name


def extract_documents_from_markdown(md_path):
    """Convert raw markdown into LangChain Document chunks."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    document = Document(page_content=content, metadata={"source": md_path})

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    return splitter.split_documents([document])

# === MAIN PIPELINE ===


def main():
    markdown_urls = get_all_markdown_urls()
    print("\nFound Markdown Files:")
    for url in markdown_urls:
        print(url)

    all_chunks = []
    for url in markdown_urls:
        print(f"\nProcessing: {url}")
        try:
            md_path = download_markdown(url)
            chunks = extract_documents_from_markdown(md_path)
            all_chunks.extend(chunks)
            os.unlink(md_path)  # Clean up
        except Exception as e:
            print(f"Error with {url}: {e}")

    print(f"\n✅ Total Chunks Created: {len(all_chunks)}")
    for i, doc in enumerate(all_chunks):
        print(f"\n--- Chunk {i + 1} ---")
        print(doc.page_content)
        print(f"Metadata: {doc.metadata}")


if __name__ == "__main__":
    main()
