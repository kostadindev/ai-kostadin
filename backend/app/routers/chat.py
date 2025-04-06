import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from app.models.query import Query

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_region = os.getenv("PINECONE_REGION", "us-east-1")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "document-index")
pc = Pinecone(api_key=pinecone_api_key)
pinecone_index = pc.Index(pinecone_index_name)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

SYSTEM_PROMPT = (
    "You are AI Kostadin and you are a chatbot for Kostadin's personal website. "
    "Answer questions about him and his work. Do not answer unrelated or inappropriate questions. "
    "If context is provided, use it to inform your answer."
)


def get_gemini_model():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is not set in the environment variables.")
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
        api_key=api_key
    )


def get_system_message():
    return SystemMessage(content=SYSTEM_PROMPT)


router = APIRouter()


@router.post("/chat")
async def chat(query: Query, gemini_model=Depends(get_gemini_model)):
    try:
        query_embedding = embeddings.embed_query(query.question)
        result = pinecone_index.query(
            vector=query_embedding,
            top_k=5,
            namespace="docs",
            include_metadata=True
        )
        matches = result.get("matches", [])
        context = ""
        for match in matches:
            metadata = match.get("metadata", {})
            text = metadata.get("text", "")
            if text:
                context += text + "\n\n"
        if context.strip():
            augmented_question = f"Context:\n{context}\nQuestion: {query.question}"
        else:
            augmented_question = query.question

        system_message = get_system_message()
        user_message = HumanMessage(content=augmented_question)

        async def token_generator():
            async for chunk in gemini_model.astream([system_message, user_message]):
                yield str(chunk.content)

        return StreamingResponse(token_generator(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
