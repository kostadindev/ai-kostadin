"""
Main FastAPI application module.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import chat
from app.config import settings

# Initialize FastAPI application
app = FastAPI(
    title="LangChain Chatbot with Gemini 2.0 Flash",
    description="A chatbot API for Kostadin's personal website using LangChain and Gemini 2.0 Flash",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/ping")
async def ping():
    """
    Health check endpoint.
    
    Returns:
        JSONResponse with a simple "pong" message.
    """
    return JSONResponse(content={"message": "pong"})

# Include routers - keeping original path structure to match frontend
app.include_router(chat.router)
