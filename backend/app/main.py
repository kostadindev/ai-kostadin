from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from fastapi.responses import JSONResponse

app = FastAPI(title="LangChain Chatbot with Gemini 2.0 Flash")

# Enable CORS for all origins (adjust as necessary)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return JSONResponse(content={"message": "pong"})

app.include_router(chat.router)
