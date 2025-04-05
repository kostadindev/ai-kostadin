import requests
import tempfile
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def download_pdf(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to download PDF. Status code: {response.status_code}")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(response.content)
    temp_file.close()
    return temp_file.name


def extract_documents_from_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Improved chunking for short structured text like a CV
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_documents(documents)


def main():
    pdf_url = "https://kostadindev.github.io/static/documents/cv.pdf"
    print(f"Downloading PDF from: {pdf_url}")
    try:
        pdf_path = download_pdf(pdf_url)
        chunks = extract_documents_from_pdf(pdf_path)
        for i, doc in enumerate(chunks):
            print(f"\n--- Chunk {i + 1} ---")
            print(doc.page_content)
            print(f"Metadata: {doc.metadata}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
