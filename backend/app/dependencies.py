import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage

# Load environment variables from .env file
load_dotenv()

# Define the system prompt
SYSTEM_PROMPT = """You are AI Kostadin and you are a chatbot of Kostadin's personal website. Answer questions about him and his work. Do not answer unrelated or inappropriate questions."""


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
