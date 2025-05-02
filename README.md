# 🚀 Artificial Me

**Artificial Me** is a personalized AI chatbot that knows everything about Kostadin's work and expertise. Embedded in his personal website, it provides intelligent, context-aware answers using **LangChain, FastAPI, and Google's Gemini 2.0 Flash model**.

## 🏗️ Project Structure

This project consists of:

- **Backend**: A FastAPI application with LangChain, Gemini, and Pinecone for RAG (Retrieval-Augmented Generation)
- **Frontend**: A React-based chat interface that communicates with the backend

## ✨ Features

- 🤖 **Personalized AI** – Trained on specific content about Kostadin's work and expertise
- 🧠 **Context-Aware Responses** – Uses RAG to provide accurate knowledge retrieval
- 💬 **Conversational Memory** – Maintains conversation context for coherent dialogue
- 🌐 **Follow-up Suggestions** – Automatically suggests relevant follow-up questions
- ⚡ **Streaming Responses** – Real-time response streaming for better user experience
- 🔄 **Multi-Environment Support** – Development and production configurations

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI
- **AI/ML**: LangChain, LangGraph
- **LLM**: Google Gemini 2.0 Flash
- **Vector Database**: Pinecone
- **Embeddings**: HuggingFace (sentence-transformers)
- **Configuration**: Pydantic Settings

### Frontend
- **Framework**: React
- **State Management**: Context API
- **Styling**: CSS Modules / Styled Components
- **UI Components**: Custom-built chat interface

## 🚀 Getting Started

See the individual README files in the `backend/` and `frontend/` directories for specific setup instructions.

### Quick Start

1. Set up the backend:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   # Set up .env file (see backend README)
   uvicorn app.main:app --reload
   ```

2. Set up the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Send messages to the chatbot and receive streaming responses |
| `POST` | `/suggest-followups` | Get follow-up question suggestions |
| `GET`  | `/ping` | Health check endpoint |
| `GET`  | `/docs` | OpenAPI documentation |

## 🧪 Future Improvements

- Add authentication for API access
- Implement rate limiting
- Add support for file uploads and processing
- Enhance the chat interface with voice input/output
- Add analytics to track common questions and improve responses
- Implement A/B testing for different system prompts

## 📖 License

This project is licensed under the **MIT License**.

---
💡 *Artificial Me – Your AI-powered personal knowledge assistant!*
