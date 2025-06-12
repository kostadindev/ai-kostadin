# 🚀 AI Kostadin
**AI Kostadin** is a personalized AI chatbot that knows everything about Kostadin's work and expertise. Embedded in his personal website, it provides intelligent, context-aware answers using **LangChain, FastAPI, and Google's Gemini 2.0 Flash model**.

> 💬 **Build Your Own!** – Anyone can use this project as a template to build a personalized chatbot that knows *them* just like AI Kostadin knows Kostadin.

> 🌐 **Access AI Kostadin** – View the chatbot embedded via iframe on [kostadindev.github.io](https://kostadindev.github.io/) or independently at [ai-kostadin.onrender.com](https://ai-kostadin.onrender.com/).

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
- **Environment Variables**:
  - `VITE_API_URL`: Backend API URL (default: http://localhost:8000)
  - `VITE_ENABLE_PARTICLES`: Enable/disable interactive particle background (default: true)
  - `VITE_APP_NAME`: Application name displayed in the header (default: "AI Kostadin")

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

## Configuration

The application uses a shared configuration system that can be accessed by both the frontend and backend. The configuration is defined in `config/config.yaml` and can be overridden using environment variables.

### Frontend Configuration

The frontend configuration is defined in `frontend/src/config/config.ts` and includes the following optional fields:

```typescript
interface Config {
  // Core UI settings
  name?: string;                    // Application name (default: "AI Kostadin")
  inputPlaceholder?: string;        // Input field placeholder text
  maxInputLength?: number;          // Maximum input length (default: 2000)
  defaultPrompts?: string[];        // Default prompt suggestions
  chatDescription?: string;         // Initial chat description (supports markdown)
  
  // Optional UI features
  features?: {
    enableParticles?: boolean;      // Enable particle background effect
    enableHexagons?: boolean;       // Enable hexagon background pattern
  }
}
```

Default values are provided for all optional fields, so you only need to specify the values you want to override.

### Backend Configuration

The backend configuration is defined in `config/config.yaml` and includes the following fields:

```yaml
backend:
  # API Configuration
  api:
    host: "0.0.0.0"                # API host
    port: 8000                     # API port
    cors_origins:                  # CORS allowed origins
      - "http://localhost:3000"
      - "http://127.0.0.1:3000"
    rate_limit:                    # Rate limiting
      requests: 100               # Number of requests
      window: 3600               # Time window in seconds

  # Document Processing
  documents:
    pdfs:
      directory: "data/pdfs"      # PDF storage directory
      chunk_size: 1000           # Text chunk size
      chunk_overlap: 200         # Chunk overlap
    images:
      directory: "data/images"   # Image storage directory
      max_size: 5242880         # Max file size (5MB)
      allowed_types:            # Allowed image types
        - "image/jpeg"
        - "image/png"
        - "image/gif"
    text:
      directory: "data/text"     # Text file storage directory
      max_size: 1048576         # Max file size (1MB)
      allowed_types:            # Allowed text file types
        - "text/plain"
        - "text/markdown"
        - "application/json"

  # Vector Database
  vector_db:
    type: "pinecone"            # Vector database type
    dimension: 1536            # Vector dimension
    metric: "cosine"           # Similarity metric
    index_name: "ai-kostadin"  # Index name
    namespace: "default"       # Namespace

  # LLM Configuration
  llm:
    model: "gpt-4"             # LLM model name
    temperature: 0.7          # Temperature
    max_tokens: 2000         # Max tokens per response
    system_prompt: "You are AI Kostadin, a helpful AI assistant."  # System prompt

  # Memory Configuration
  memory:
    type: "buffer"            # Memory type
    max_tokens: 2000         # Max tokens in memory
    return_messages: true    # Return messages in memory

  # Search Configuration
  search:
    type: "similarity"       # Search type
    k: 4                    # Number of results
    score_threshold: 0.7    # Similarity threshold

  # Logging Configuration
  logging:
    level: "INFO"           # Log level
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Log format
    file: "logs/app.log"    # Log file path
```

### Environment Variables

All configuration values can be overridden using environment variables. The naming convention is:
- Frontend: `UI_<SECTION>_<FIELD>` (e.g., `UI_NAME`, `UI_FEATURES_ENABLE_PARTICLES`)
- Backend: `BACKEND_<SECTION>_<FIELD>` (e.g., `BACKEND_API_PORT`, `BACKEND_LLM_MODEL`)

Example:
```bash
# Frontend
UI_NAME="My AI Assistant"
UI_FEATURES_ENABLE_PARTICLES=true

# Backend
BACKEND_API_PORT=8080
BACKEND_LLM_MODEL="gpt-3.5-turbo"
```

### Configuration Adapters

The configuration system includes adapters for both Python and TypeScript:

- Python: `config/config.py` - Uses Pydantic for validation and environment variable loading
- TypeScript: `frontend/src/config/config.ts` - Uses TypeScript's type system for type safety

Both adapters provide:
- Type safety
- Default values
- Environment variable overrides
- Optional field handling
