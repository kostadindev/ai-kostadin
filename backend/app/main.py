from fastapi import FastAPI
from app.routers import chat

app = FastAPI(title="LangChain Chatbot with Gemini 2.0 Flash")

app.include_router(chat.router)
