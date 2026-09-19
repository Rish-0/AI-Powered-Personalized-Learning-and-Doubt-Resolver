# 🎓 AI-Powered Personalized Learning & Doubt Resolver

An intelligent AI tutoring system that provides **personalized, context-aware answers** to student queries by leveraging uploaded study materials (PDFs), web search, and general knowledge — all adapted to each student's difficulty level and learning style.

---

## ✨ Features

- **📄 PDF-Based Q&A (RAG)** — Upload your study materials and ask questions directly from them. The system retrieves relevant chunks and generates accurate, citation-backed answers.
- **🌐 Web Search Integration** — Queries about current events, latest technologies, or trending topics are answered using real-time web search via the Tavily API.
- **💬 General Chat** — General knowledge questions, coding help, and conceptual explanations are handled directly by the LLM.
- **🤖 Intelligent Query Routing** — A router agent automatically classifies each question and dispatches it to the appropriate pipeline (PDF_RAG / WEB_SEARCH / GENERAL_CHAT).
- **👤 Student Personalization** — Responses are tailored based on:
  - Difficulty level (Beginner / Intermediate / Advanced)
  - Learning style (Visual / Textual / Example-based / Step-by-step)
  - Known weak & strong topics
- **🧠 Conversation Memory** — Maintains context across messages for coherent follow-up conversations.
- **📊 Chat History** — Previous conversations are saved and can be revisited.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend (HTML/CSS/JS)             │
│         Chat UI · PDF Upload · Profile Settings         │
└──────────────────────┬──────────────────────────────────┘
                       │  REST API
┌──────────────────────▼──────────────────────────────────┐
│                   FastAPI Backend                        │
│  ┌──────────────────────────────────────────────────┐   │
│  │              LangGraph Workflow                   │   │
│  │                                                   │   │
│  │   ┌──────────┐    ┌─────────┐    ┌────────────┐  │   │
│  │   │  Router  │───▶│ PDF_RAG │    │ WEB_SEARCH │  │   │
│  │   │  Agent   │───▶│         │    │            │  │   │
│  │   │          │───▶│ GENERAL │    │            │  │   │
│  │   └──────────┘    └─────────┘    └────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌────────────┐  ┌─────────┐  ┌───────────────────┐    │
│  │   FAISS    │  │  Groq   │  │  Personalization  │    │
│  │  Vector DB │  │   LLM   │  │     Service       │    │
│  └────────────┘  └─────────┘  └───────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

### Workflow

1. **User asks a question** via the chat interface.
2. The **Router Agent** (LLM-based) classifies the query into one of three routes:
   - `PDF_RAG` → Retrieves context from uploaded PDFs via FAISS, injects student profile & conversation memory, and generates a personalized answer.
   - `WEB_SEARCH` → Fetches top results from Tavily API and synthesizes an answer.
   - `GENERAL_CHAT` → Answers directly using the LLM.
3. The response is returned with **source citations** and the **route used**.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | [Groq](https://groq.com/) (fast inference — LLaMA 3 / Mixtral) |
| **Embeddings** | [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) via HuggingFace |
| **Vector Store** | [FAISS](https://github.com/facebookresearch/faiss) (local similarity search) |
| **Orchestration** | [LangGraph](https://github.com/langchain-ai/langgraph) (state-machine workflow) |
| **RAG Framework** | [LangChain](https://github.com/langchain-ai/langchain) |
| **Web Search** | [Tavily API](https://tavily.com/) |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) (Python) |
| **Frontend** | Vanilla HTML / CSS / JavaScript |
| **Database** | SQLite (profiles, memory, history) |
| **Markdown Rendering** | [Marked.js](https://marked.js.org/) |

---

## 📁 Project Structure

```
AI-Powered-Personalized-Learning-and-Doubt-Resolver/
├── frontend/
│   ├── index.html              # Main UI
│   ├── styles.css              # Styling (glassmorphism, animations)
│   └── app.js                  # Client-side logic
│
├── backend/
│   ├── requirements.txt        # Python dependencies
│   └── app/
│       ├── main.py             # FastAPI app entry point
│       ├── .env                # API keys (GROQ, TAVILY, MODEL_NAME)
│       │
│       ├── api/                # REST endpoints
│       │   ├── chat.py         # POST /api/chat
│       │   ├── upload.py       # POST /api/upload
│       │   ├── retrieval.py    # Retrieval endpoints
│       │   ├── router.py       # Router agent endpoint
│       │   ├── profile.py      # Student profile CRUD
│       │   └── history.py      # Conversation history
│       │
│       ├── graph/              # LangGraph workflow
│       │   ├── workflow.py     # Graph definition & compilation
│       │   ├── nodes.py        # Node functions (router, pdf, web, chat)
│       │   ├── edges.py        # Conditional edge routing
│       │   └── state.py        # GraphState TypedDict
│       │
│       ├── services/
│       │   ├── agents/         # Router agent & prompt
│       │   ├── llm/            # Groq LLM service
│       │   ├── embeddings/     # HuggingFace embeddings
│       │   ├── vectorstore/    # FAISS index management
│       │   ├── retrieval/      # Document retriever
│       │   ├── rag/            # RAG pipeline & prompt builder
│       │   ├── search/         # Tavily web search
│       │   ├── memory/         # Conversation memory & history
│       │   ├── personalization/# Profile-based response tuning
│       │   ├── profile/        # Student profile management
│       │   ├── parser/         # PDF parsing
│       │   ├── chunking/       # Document chunking
│       │   ├── indexing/       # FAISS indexing pipeline
│       │   └── file/           # File upload handling
│       │
│       ├── core/
│       │   └── config.py       # App settings & env vars
│       │
│       ├── database/
│       │   └── sqlite.py       # SQLite connection
│       │
│       ├── models/             # Data models
│       └── schemas/            # Pydantic schemas
│
└── uploaded_files/             # Stored uploaded PDFs
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Groq API Key](https://console.groq.com/)
- [Tavily API Key](https://tavily.com/) (for web search)

### 1. Clone the Repository

```bash
git clone https://github.com/Rish-0/AI-Powered-Personalized-Learning-and-Doubt-Resolver.git
cd AI-Powered-Personalized-Learning-and-Doubt-Resolver
```

### 2. Set Up the Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create/edit `backend/app/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
MODEL_NAME=llama3-70b-8192
```

### 4. Run the Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. You can visit `http://localhost:8000/docs` for the interactive Swagger UI.

### 5. Open the Frontend

Open `frontend/index.html` in your browser, or serve it with any static file server:

```bash
cd frontend
python -m http.server 5500
```

Then visit `http://localhost:5500`.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/chat` | Send a question and get an AI-generated answer |
| `POST` | `/api/upload` | Upload a PDF study material |
| `GET` | `/api/retrieval` | Retrieve relevant document chunks |
| `POST` | `/api/route` | Classify a query into a route |
| `GET/POST` | `/api/profile` | Get or update student profile |
| `GET` | `/api/history` | Fetch conversation history |
| `GET` | `/health` | Health check |

### Example: Chat Request

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"username": "student", "question": "Explain deadlock in operating systems"}'
```

**Response:**
```json
{
  "question": "Explain deadlock in operating systems",
  "answer": "A deadlock is a situation where two or more processes are ...",
  "route": "PDF_RAG",
  "sources": [
    {"page": 42, "source": "OS_textbook.pdf"}
  ]
}
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is developed as part of a university course (7th Semester). Feel free to use it for educational purposes.

---

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) & [LangGraph](https://github.com/langchain-ai/langgraph) for the RAG and orchestration framework
- [Groq](https://groq.com/) for blazing-fast LLM inference
- [Tavily](https://tavily.com/) for the web search API
- [FAISS](https://github.com/facebookresearch/faiss) by Meta AI for vector similarity search
- [HuggingFace](https://huggingface.co/) for the embedding model
