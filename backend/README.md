# Artificial-Me Backend

A FastAPI-based chatbot backend using LangChain, Gemini 2.0 Flash, and Pinecone for retrieval-augmented generation (RAG).

## Features

- **Gemini 2.0 Flash Integration**: Advanced AI chat capabilities powered by Google's Gemini 2.0 Flash model
- **Context-aware Responses**: Uses RAG (Retrieval-Augmented Generation) to provide context-aware answers
- **Vector Database**: Pinecone integration for efficient similarity search
- **Follow-up Suggestions**: Automatic generation of relevant follow-up questions
- **Streaming Responses**: Real-time streaming of chat responses
- **Environment Management**: Multi-environment support (development/production)

## Architecture

The backend follows a clean, modular architecture:

- **Configuration Management**: Centralized settings via Pydantic
- **Service Layer**: Dedicated services for embeddings, Pinecone, and Gemini
- **API Endpoints**: FastAPI routes with proper error handling
- **LangGraph Integration**: Advanced workflow for chat processing

## Getting Started

### Prerequisites

- Python 3.8+
- API keys for Google Gemini, HuggingFace, and Pinecone

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file in the backend directory with the following values:

```
ENV=development
GOOGLE_API_KEY=your_gemini_api_key
HF_API_TOKEN=your_huggingface_token
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_API_REGION=us-east-1  # Use your region
PINECONE_API_INDEX=document-index  # Use your index name
```

### Running the Application

**Development Mode**:
```bash
uvicorn app.main:app --reload
```

**Production Mode**:
```bash
ENV=production uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Using Docker**:
```bash
docker build -t artificial-me-backend .
docker run -p 8000:8000 artificial-me-backend
```

## API Endpoints

### Chat

- **POST** `/chat`
  - Processes chat messages and returns AI responses
  - Request body: `{ "history": [{"role": "user", "content": "Your message"}] }`
  - Returns: Streaming text response

### Follow-up Suggestions

- **POST** `/suggest-followups`
  - Generates relevant follow-up questions based on chat history
  - Request body: `{ "history": [{"role": "user", "content": "Your message"}, {"role": "assistant", "content": "Response"}] }`
  - Returns: `{ "suggestions": ["Question 1", "Question 2"] }`

### Health Check

- **GET** `/ping`
  - Returns: `{ "message": "pong" }`

## Development

### Project Structure

```
app/
├── config.py           # Configuration settings
├── dependencies.py     # Dependency management (deprecated)
├── main.py             # FastAPI application entrypoint
├── __init__.py
├── models/             # Data models
├── routers/            # API routes
│   └── chat.py         # Chat endpoints
└── services/           # Business logic
    ├── embeddings.py   # Text embedding service
    ├── gemini.py       # LLM service
    └── pinecone.py     # Vector database service
```

### Adding New Features

1. Create any necessary models in `app/models/`
2. Implement business logic in appropriate service files
3. Add API endpoints in relevant router files
4. Import and include routers in `main.py`

## Deployment

### Docker

The application includes a Dockerfile for easy containerization:

```bash
docker build -t artificial-me-backend .
docker run -p 8000:8000 artificial-me-backend
```

### Environment Variables

For production deployments, ensure the following environment variables are set:
- `ENV=production`
- `GOOGLE_API_KEY`
- `HF_API_TOKEN`
- `PINECONE_API_KEY`
- `PINECONE_API_REGION`
- `PINECONE_API_INDEX`

## License

This project is licensed under the MIT License - see the LICENSE file for details. 