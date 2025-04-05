import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables
load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_region = os.getenv("PINECONE_REGION", "us-east-1")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "document-index")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)

# Define test queries
queries = [
    "What machine learning experience does Kostadin have?",
    "Which programming languages does Kostadin use?",
    "Where has Kostadin worked?",
    "What degrees or education has Kostadin received?",
    "Does Kostadin have experience with AI or data science?",
    "Mention projects involving NLP or computer vision."
]

# Run retrieval
for query in queries:
    print("\n========================")
    print(f"🔍 Query: {query}")

    # Embed query
    embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={"input_type": "query"}
    )

    # Search Pinecone
    results = index.query(
        namespace="docs",
        vector=embedding[0].values,
        top_k=3,
        include_metadata=True,
        include_values=False
    )

    # Print results
    if not results.matches:
        print("❌ No results found.")
    else:
        for i, match in enumerate(results.matches, 1):
            text_snippet = match.metadata['text'][:200].strip().replace(
                "\n", " ")
            print(f"\n✅ Match {i} (score: {match.score:.4f})")
            print(f"{text_snippet}...")
