# 🎓 AI-Powered Personalized Learning & Doubt Resolver

An intelligent AI tutoring system that lets students **upload their study material (PDF)** and then **ask any doubt** about it. The system retrieves the most relevant passages from the uploaded document using vector similarity search (RAG — Retrieval-Augmented Generation), feeds them to a large language model, and generates a **document-grounded, citation-backed answer** — all adapted to each student's difficulty level and learning style.

---

## 📌 Table of Contents

- [What This Project Does](#-what-this-project-does)
- [How It Works — End-to-End Flow](#-how-it-works--end-to-end-flow)
- [Architecture Diagram](#-architecture-diagram)
- [Tech Stack](#-tech-stack)
- [Project Structure — Every File Explained](#-project-structure--every-file-explained)
- [Detailed Component Breakdown](#-detailed-component-breakdown)
  - [1. Streamlit Frontend](#1-streamlit-frontend-streamlit_apppy)
  - [2. FastAPI Backend](#2-fastapi-backend-backendappmainpy)
  - [3. PDF Ingestion Pipeline](#3-pdf-ingestion-pipeline)
  - [4. LangGraph Workflow Engine](#4-langgraph-workflow-engine)
  - [5. RAG Pipeline](#5-rag-pipeline-retrieval-augmented-generation)
  - [6. Student Personalization](#6-student-personalization)
  - [7. Conversation Memory & History](#7-conversation-memory--history)
  - [8. Database Layer](#8-database-layer)
- [Getting Started — Installation & Run Commands](#-getting-started--installation--run-commands)
- [Environment Variables](#-environment-variables)
- [API Endpoints Reference](#-api-endpoints-reference)
- [Screenshots & User Flow](#-screenshots--user-flow)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 What This Project Does

Imagine you have a 300-page textbook PDF and an exam tomorrow. Instead of reading the entire thing, you:

1. **Upload the PDF** → The system parses every page, splits the text into small overlapping chunks, converts each chunk into a numerical vector (embedding), and stores them in a FAISS vector index.
2. **Ask a doubt** (e.g., *"Explain the difference between TCP and UDP"*) → The system searches the vector index to find the 6 most relevant chunks from your PDF, then sends those chunks + your question to an LLM which generates a detailed answer **strictly grounded in your document**, with page number citations.
3. **Personalize your profile** → Set your difficulty level (Beginner/Intermediate/Advanced) and preferred learning style (Visual/Textual/Example-based/Step-by-step). The AI adapts its tone, depth, and explanation format accordingly.

**Key Design Decision:** Once a PDF is uploaded and indexed, **all queries are routed through the PDF-RAG pipeline**. The system does NOT use external knowledge or the internet — every answer comes exclusively from your uploaded document with explicit page citations. If the answer isn't in the PDF, it tells you so.

---

## 🔄 How It Works — End-to-End Flow

```
Student uploads PDF
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  PDF INGESTION PIPELINE                                     │
│                                                             │
│  FileService         → saves PDF to disk                    │
│  PDFParser (PyMuPDF) → extracts text from each page         │
│  TextCleaner         → removes noise, extra whitespace      │
│  TextChunker         → splits into 500-char chunks          │
│                        with 100-char overlap                 │
│  EmbeddingService    → BAAI/bge-small-en-v1.5 (384-dim)    │
│  FAISSService        → creates & saves vector index         │
└─────────────────────────────────────────────────────────────┘
       │
       ▼  (Index saved to disk)
   Student asks a doubt
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  LANGGRAPH WORKFLOW                                         │
│                                                             │
│  RouterNode → checks if FAISS index exists                  │
│      │        → YES: force route = "PDF_RAG"                │
│      │        → NO:  ask LLM to classify the query          │
│      ▼                                                      │
│  PDF Node (RAG Pipeline)                                    │
│      │                                                      │
│      ├─ RetrieverService → similarity search (top 6 chunks) │
│      ├─ ContextBuilder   → formats chunks with page numbers │
│      ├─ ConversationService → loads last 5 Q&A pairs        │
│      ├─ PersonalizationService → loads student profile       │
│      ├─ PromptBuilder    → assembles the final prompt       │
│      │   (strict instructions: answer ONLY from document,   │
│      │    cite page numbers, adapt to student profile)      │
│      ├─ GroqService      → sends prompt to LLM via Groq    │
│      └─ MemoryService    → saves Q&A to SQLite             │
│                                                             │
│  Response: answer + route + source citations                │
└─────────────────────────────────────────────────────────────┘
       │
       ▼
  Streamlit UI renders the answer with
  route badge, markdown formatting, and
  expandable source citations with page numbers
```

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit UI (Python)                  │
│       Chat Interface · PDF Upload · Profile Settings     │
└──────────────────────┬──────────────────────────────────┘
                       │  REST API (HTTP)
                       │  Port 8501 → Port 8000
┌──────────────────────▼──────────────────────────────────┐
│                   FastAPI Backend                         │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │              LangGraph State Machine                │  │
│  │                                                     │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────────┐  │  │
│  │  │  Router  │───▶│ PDF_RAG  │    │  WEB_SEARCH  │  │  │
│  │  │  Node    │    │  Node    │    │  Node        │  │  │
│  │  │          │    │          │    │              │  │  │
│  │  │          │───▶│ GENERAL  │    │              │  │  │
│  │  └──────────┘    │  CHAT    │    └──────────────┘  │  │
│  │                  └──────────┘                       │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────┐  ┌──────────┐  ┌───────────────────┐   │
│  │   FAISS    │  │  Groq    │  │  Personalization  │   │
│  │ Vector DB  │  │  LLM API │  │     Service       │   │
│  └────────────┘  └──────────┘  └───────────────────┘   │
│                                                          │
│  ┌────────────┐  ┌──────────────────────────────────┐   │
│  │  SQLite DB │  │  Conversation Memory Service      │   │
│  │ (Profiles  │  │  (Last 5 Q&A pairs as context)    │   │
│  │  & History)│  │                                    │   │
│  └────────────┘  └──────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive Python web UI with chat interface, file uploader, and profile settings |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com/) | REST API server handling all business logic endpoints |
| **LLM Inference** | [Groq](https://groq.com/) | Ultra-fast LLM inference (supports LLaMA 3, Mixtral, GPT-compatible models) |
| **Embeddings** | [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) | 384-dimensional sentence embeddings via HuggingFace for semantic search |
| **Vector Store** | [FAISS](https://github.com/facebookresearch/faiss) | Facebook's library for efficient similarity search on embedding vectors |
| **Workflow Engine** | [LangGraph](https://github.com/langchain-ai/langgraph) | State-machine graph that routes queries through the correct processing pipeline |
| **RAG Framework** | [LangChain](https://github.com/langchain-ai/langchain) | Document loaders, text splitters, retrievers, and vector store integrations |
| **PDF Parsing** | [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) | Fast, accurate text extraction from PDF files |
| **Web Search** | [Tavily API](https://tavily.com/) | Real-time web search (available as fallback when no PDF is indexed) |
| **Database** | [SQLite](https://sqlite.org/) | Lightweight local database for student profiles and conversation history |
| **Markdown** | Built-in Streamlit | Renders LLM responses with tables, code blocks, bold text, and lists |

---

## 📁 Project Structure — Every File Explained

```
AI-Powered-Personalized-Learning-and-Doubt-Resolver/
│
├── streamlit_app.py               # 🖥️  Main Streamlit UI (3-step guided workflow)
├── app.py                         # 🔗  Alternate entrypoint (imports streamlit_app)
├── requirements.txt               # 📦  Root-level dependencies (references backend)
├── README.md                      # 📖  This file
├── .gitignore                     # 🚫  Git ignore rules
│
└── backend/
    ├── requirements.txt           # 📦  All Python dependencies (pip install -r)
    │
    └── app/
        ├── main.py                # 🚀  FastAPI application entry point
        │                          #     Creates the app, adds CORS middleware,
        │                          #     and mounts all API routers
        ├── __init__.py            # 📦  Python package marker
        ├── .env                   # 🔑  API keys (GROQ_API_KEY, TAVILY_API_KEY, MODEL_NAME)
        │
        ├── core/
        │   ├── config.py          # ⚙️  Loads .env, creates Settings object
        │   │                      #     with GROQ_API_KEY, TAVILY_API_KEY, MODEL_NAME
        │   └── constants.py       # 📏  ALLOWED_EXTENSIONS=[".pdf"], MAX_FILE_SIZE=20MB,
        │                          #     UPLOAD_DIRECTORY="uploaded_files"
        │
        ├── database/
        │   └── sqlite.py          # 🗄️  SQLite connection factory
        │                          #     Creates data/memory.db, sets row_factory=sqlite3.Row
        │
        ├── api/                   # 🌐  REST API endpoint routers
        │   ├── chat.py            # POST /api/chat — accepts {username, question},
        │   │                      #   invokes the LangGraph workflow, returns
        │   │                      #   {question, answer, route, sources}
        │   ├── upload.py          # POST /api/upload — accepts a PDF file,
        │   │                      #   triggers the full indexing pipeline
        │   ├── profile.py         # GET /api/profile/{username} — fetch profile
        │   │                      # POST /api/profile — create/update profile
        │   ├── history.py         # GET /api/history?limit=20 — recent Q&A pairs
        │   ├── retrieval.py       # GET /api/retrieval — direct retrieval endpoint
        │   └── router.py         # POST /api/route — classify a query
        │
        ├── graph/                 # 🔀  LangGraph state machine (the brain)
        │   ├── state.py           # 📋  GraphState TypedDict defining the state shape:
        │   │                      #     {username, question, route, profile, memory,
        │   │                      #      context, answer, sources}
        │   ├── workflow.py        # 🏗️  Builds & compiles the LangGraph:
        │   │                      #     entry → router → (pdf|web|chat) → END
        │   ├── nodes.py           # ⚡  Node functions:
        │   │                      #     router_node: if FAISS index exists → force PDF_RAG
        │   │                      #     pdf_node: invokes RAGService.ask()
        │   │                      #     web_node: Tavily search → LLM summarize
        │   │                      #     chat_node: direct LLM response
        │   └── edges.py           # 🔗  route_edge: returns state["route"] to select
        │                          #     which node to execute next
        │
        ├── schemas/               # 📐  Pydantic request/response schemas
        │
        └── services/              # 🧩  All business logic services
            │
            ├── file/
            │   └── file_service.py        # 💾  Validates file type & size, saves PDF
            │                              #     to uploaded_files/ with UUID filename
            │
            ├── parser/
            │   ├── pdf_parser.py          # 📄  Uses PyMuPDF (fitz) to extract text
            │   │                          #     from each page of the PDF
            │   └── cleaner.py             # 🧹  TextCleaner: removes extra whitespace,
            │                              #     excessive blank lines, trims text
            │
            ├── chunking/
            │   ├── text_chunker.py        # ✂️  RecursiveCharacterTextSplitter:
            │   │                          #     chunk_size=500, overlap=100
            │   │                          #     Splits on: \n\n → \n → ". " → " " → ""
            │   └── metadata.py            # 🏷️  ChunkMetadata: assigns each chunk a
            │                              #     UUID, source filename, page number,
            │                              #     and chunk_index
            │
            ├── embeddings/
            │   └── embedding_service.py   # 🧮  Loads BAAI/bge-small-en-v1.5 model
            │                              #     from HuggingFace (384-dim vectors,
            │                              #     normalized, CPU inference)
            │
            ├── vectorstore/
            │   └── faiss_service.py       # 📊  FAISS vector database:
            │                              #     create() — builds index from documents
            │                              #     save()   — persists to vector_store/faiss_index/
            │                              #     load()   — loads from disk
            │
            ├── retrieval/
            │   ├── retriever.py           # 🔍  RetrieverService: wraps FAISS as a
            │   │                          #     LangChain retriever (similarity search, k=6)
            │   │                          #     Auto-reloads when index file changes
            │   └── context_builder.py     # 📝  Formats retrieved documents into a string:
            │                              #     "Source: file.pdf | Page: 5 | <content>"
            │
            ├── rag/
            │   ├── rag_service.py         # 🧠  The core RAG orchestrator:
            │   │                          #     1. Retrieve relevant chunks
            │   │                          #     2. Build context string
            │   │                          #     3. Load conversation memory
            │   │                          #     4. Load student profile
            │   │                          #     5. Assemble prompt via PromptBuilder
            │   │                          #     6. Send to LLM via GroqService
            │   │                          #     7. Save Q&A to memory
            │   │                          #     8. Return answer + sources
            │   ├── prompt_builder.py      # 📋  Constructs the LLM prompt with strict
            │   │                          #     instructions: answer ONLY from document,
            │   │                          #     cite page numbers, adapt to student profile
            │   └── prompt_context.py      # 📦  PromptContext dataclass holding all
            │                              #     prompt ingredients: question, context,
            │                              #     memory, profile, sources
            │
            ├── agents/
            │   ├── router_agent.py        # 🤖  LLM-based query classifier (used as
            │   │                          #     fallback when no FAISS index exists)
            │   └── router_prompt.py       # 📜  Prompt template for classification:
            │                              #     → PDF_RAG, WEB_SEARCH, or GENERAL_CHAT
            │
            ├── search/
            │   └── tavily_service.py      # 🌐  Tavily web search client
            │                              #     (advanced depth, max 5 results)
            │
            ├── llm/
            │   └── groq_service.py        # ⚡  Groq LLM client: sends prompts to the
            │                              #     configured model (temperature=0.2,
            │                              #     max_tokens=1024)
            │
            ├── memory/
            │   ├── memory_service.py      # 💾  SQLite-backed conversation storage:
            │   │                          #     save(question, answer, route)
            │   │                          #     history(limit) → recent Q&A pairs
            │   └── conversation_service.py # 🔄  Formats last 5 Q&A pairs into a
            │                              #     context string for the LLM prompt
            │
            ├── personalization/
            │   └── personalization_service.py  # 👤  Loads student profile and formats
            │                                   #     it into a context block:
            │                                   #     difficulty, learning_style,
            │                                   #     weak_topics, strong_topics
            │
            ├── profile/
            │   └── profile_service.py     # 👤  CRUD operations on student_profile
            │                              #     table in SQLite (create_user,
            │                              #     update_profile, get_profile)
            │
            └── indexing/
                └── indexing_service.py     # 🔧  Orchestrates the full PDF→FAISS pipeline:
                                           #     FileService → PDFParser → TextChunker
                                           #     → FAISSService.create() → FAISSService.save()
                                           #     Returns {pages, chunks, file}
```

---

## 🔬 Detailed Component Breakdown

### 1. Streamlit Frontend (`streamlit_app.py`)

The user interface follows a **3-step guided workflow**:

| Step | What Happens | UI Component |
|------|-------------|-------------|
| **Step 1: Upload PDF** | Student uploads a textbook/notes PDF. The system indexes it into FAISS. This step is **mandatory** — the chat interface is locked until a PDF is uploaded. | File uploader with progress, success message showing pages & chunks indexed |
| **Step 2: Ask Doubts** | Student types questions in the chat. Every answer cites the exact pages from the uploaded document. | Full chat interface with `st.chat_message`, route badges, expandable source citations |
| **Step 3: Personalize (Optional)** | Student can set difficulty level, learning style, weak/strong topics. After asking doubts, a nudge banner appears suggesting to personalize. | Expandable profile form in the main content area |

**Key UI features:**
- **Active Document Banner** — always shows which PDF is active, with page/chunk stats
- **Route Badge** — colored pill showing how the answer was sourced (`📄 PDF RAG`, `🌐 Web Search`, `💬 General`)
- **Source Citations** — expandable section listing the exact PDF pages used
- **Starter Suggestions** — context-aware quick prompts like *"Summarize key concepts from {document}"*
- **Stepper Navigation** — visual progress bar showing which step the student is on
- **Sidebar** — shows current workflow status, uploaded materials list, past conversation history

### 2. FastAPI Backend (`backend/app/main.py`)

The backend is a standard **FastAPI** application that:
- Adds **CORS middleware** (allows all origins for local development)
- Mounts **6 API routers** under the `/api` prefix: chat, upload, retrieval, router, profile, history
- Exposes a **health check** endpoint at `GET /health`

### 3. PDF Ingestion Pipeline

When a student uploads a PDF, the following pipeline executes:

```
PDF File
  │
  ▼
FileService.save_pdf()
  │  • Validates extension (.pdf only)
  │  • Validates size (≤ 20 MB)
  │  • Saves to uploaded_files/ with UUID name
  ▼
PDFParser.extract_text()
  │  • Opens PDF with PyMuPDF (fitz)
  │  • Iterates through every page
  │  • Extracts raw text from each page
  │  • Cleans text (TextCleaner: remove extra spaces, blank lines)
  │  • Returns list of {page, source, text}
  ▼
TextChunker.chunk_pages()
  │  • Uses LangChain's RecursiveCharacterTextSplitter
  │  • chunk_size = 500 characters
  │  • chunk_overlap = 100 characters (ensures no information loss at boundaries)
  │  • Split hierarchy: paragraphs → lines → sentences → words → characters
  │  • Each chunk gets metadata: {chunk_id (UUID), source, page, chunk_index}
  │  • Returns list of LangChain Document objects
  ▼
FAISSService.create()
  │  • Converts all chunks into 384-dimensional vectors
  │    using BAAI/bge-small-en-v1.5 embeddings
  │  • Builds a FAISS index for fast similarity search
  ▼
FAISSService.save()
     • Persists the index to disk at vector_store/faiss_index/
     • Can be reloaded without re-processing the PDF
```

### 4. LangGraph Workflow Engine

The query processing is orchestrated by a **LangGraph state machine** — a directed graph where:

- **Nodes** are functions that transform the state
- **Edges** determine which node runs next
- **State** is a `TypedDict` carrying: `username`, `question`, `route`, `profile`, `memory`, `context`, `answer`, `sources`

```
                    ┌─────────┐
        Entry ────▶ │ Router  │
                    │  Node   │
                    └────┬────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         ┌────────┐ ┌────────┐ ┌────────┐
         │PDF_RAG │ │  WEB   │ │GENERAL │
         │ Node   │ │SEARCH  │ │ CHAT   │
         │        │ │ Node   │ │ Node   │
         └───┬────┘ └───┬────┘ └───┬────┘
             │          │          │
             ▼          ▼          ▼
                    ┌─────────┐
                    │   END   │
                    └─────────┘
```

**Router Logic (router_node):**
1. Check if a FAISS index exists on disk → if YES, **force** `route = "PDF_RAG"` (all queries go to the PDF)
2. If NO index exists → use the LLM-based `RouterAgent` to classify the query into `PDF_RAG`, `WEB_SEARCH`, or `GENERAL_CHAT`

This ensures that once a student has uploaded a PDF, **every question is answered from that document**.

### 5. RAG Pipeline (Retrieval-Augmented Generation)

This is the core intelligence of the system. When a doubt is asked:

1. **Retrieve** — `RetrieverService` performs FAISS similarity search to find the top 6 most relevant document chunks
2. **Build Context** — `ContextBuilder` formats each chunk as `"Source: file.pdf | Page: 5 | <content>"` 
3. **Load Memory** — `ConversationService` fetches the last 5 Q&A pairs so the LLM understands follow-up questions
4. **Load Profile** — `PersonalizationService` fetches the student's difficulty level, learning style, and topic preferences
5. **Build Prompt** — `PromptBuilder` assembles the final prompt with **strict instructions**:
   - Answer EXCLUSIVELY from the uploaded document context
   - ALWAYS cite page numbers (e.g., `[Page 5]`, `[Pages 8-9]`)
   - If the answer isn't in the document, say so explicitly
   - Adapt tone/depth/format to the student's profile
6. **Generate** — `GroqService` sends the prompt to the LLM via the Groq API (temperature=0.2 for factual accuracy)
7. **Save** — `MemoryService` persists the Q&A pair to SQLite for history

### 6. Student Personalization

Each student has a profile stored in SQLite with:

| Field | Options | Effect on Answers |
|-------|---------|-------------------|
| **difficulty** | `beginner`, `medium`, `advanced` | Beginner = simple language, more analogies; Advanced = technical depth, assumes prerequisites |
| **learning_style** | `textual`, `visual`, `example-based`, `step-by-step` | Textual = detailed paragraphs; Visual = structured tables/diagrams; Example-based = concrete examples; Step-by-step = numbered walkthrough |
| **weak_topics** | Free text (e.g., "Recursion, Pointers") | AI provides extra guidance and simpler explanations for these topics |
| **strong_topics** | Free text (e.g., "Python, Arrays") | AI skips basic definitions and goes straight to advanced aspects |

### 7. Conversation Memory & History

- **ConversationService** — Maintains a rolling window of the last 5 Q&A pairs. This context is injected into every prompt so the LLM can understand follow-up questions (e.g., *"Explain that in more detail"* or *"What about the second point?"*)
- **MemoryService** — Saves every Q&A exchange with its route (`PDF_RAG`, `WEB_SEARCH`, `GENERAL_CHAT`) and timestamp to the `conversations` table in SQLite
- **History API** — The Streamlit sidebar can fetch and display past conversations, allowing students to revisit previous answers

### 8. Database Layer

A single **SQLite** database (`data/memory.db`) with two tables:

```sql
-- Stores every Q&A exchange
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    question TEXT,
    answer TEXT,
    route TEXT,                    -- PDF_RAG | WEB_SEARCH | GENERAL_CHAT
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stores student learning profiles
CREATE TABLE student_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    difficulty TEXT DEFAULT 'medium',
    learning_style TEXT DEFAULT 'visual',
    weak_topics TEXT DEFAULT '',
    strong_topics TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🚀 Getting Started — Installation & Run Commands

### Prerequisites

- **Python 3.10+** installed
- **[Groq API Key](https://console.groq.com/)** — free tier available for fast LLM inference
- **[Tavily API Key](https://tavily.com/)** — free tier available for web search (optional, used only when no PDF is indexed)

### 1. Clone the Repository

```bash
git clone https://github.com/Rish-0/AI-Powered-Personalized-Learning-and-Doubt-Resolver.git
cd AI-Powered-Personalized-Learning-and-Doubt-Resolver
```

### 2. Create & Activate Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate          # Windows (PowerShell / CMD)
# source venv/bin/activate     # macOS / Linux
```

### 3. Install All Dependencies

```bash
pip install -r requirements.txt
pip install streamlit
```

### 4. Configure API Keys

Create or edit the file `backend/app/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
MODEL_NAME=llama3-70b-8192
```

> You can get a free Groq API key at [console.groq.com](https://console.groq.com/) and a free Tavily key at [tavily.com](https://tavily.com/).

### 5. Start the Backend Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Verify it's running: visit **http://localhost:8000/docs** for the Swagger API docs.

### 6. Start the Streamlit UI (New Terminal)

Open a **new terminal window**, navigate to the project root, and run:

```bash
cd AI-Powered-Personalized-Learning-and-Doubt-Resolver
streamlit run streamlit_app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

### 7. Open in Browser

Visit **http://localhost:8501** — you'll see the guided 3-step workflow:

1. Upload your PDF
2. Ask your doubts
3. Optionally personalize your profile

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ Yes | API key for Groq LLM inference. Get it free at [console.groq.com](https://console.groq.com/) |
| `TAVILY_API_KEY` | ⚠️ Optional | API key for Tavily web search. Only needed if you want web search fallback |
| `MODEL_NAME` | ✅ Yes | The LLM model to use. Examples: `llama3-70b-8192`, `mixtral-8x7b-32768`, `llama3-8b-8192` |

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|-------------|----------|
| `GET` | `/` | Root — API status check | — | `{"message": "AI Tutor API Running"}` |
| `GET` | `/health` | Health check | — | `{"status": "healthy"}` |
| `POST` | `/api/chat` | Ask a question | `{"username": "student", "question": "..."}` | `{"question", "answer", "route", "sources"}` |
| `POST` | `/api/upload` | Upload & index a PDF | `multipart/form-data` with `file` field | `{"message", "pages", "chunks", "file"}` |
| `GET` | `/api/profile/{username}` | Get student profile | — | `{"username", "difficulty", "learning_style", ...}` |
| `POST` | `/api/profile` | Create/update profile | `{"username", "difficulty", "learning_style", "weak_topics", "strong_topics"}` | Updated profile object |
| `GET` | `/api/history?limit=20` | Get conversation history | — | Array of `{"id", "question", "answer", "route", "created_at"}` |

### Example: Ask a Doubt via cURL

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"username": "student", "question": "Explain the OSI model layers"}'
```

**Response:**
```json
{
  "question": "Explain the OSI model layers",
  "answer": "According to the uploaded document, the OSI model consists of 7 layers... [Page 3] ...",
  "route": "PDF_RAG",
  "sources": [
    {"page": 3, "source": "networking_notes.pdf"},
    {"page": 4, "source": "networking_notes.pdf"}
  ]
}
```

---

## 🖼️ Screenshots & User Flow

### Step 1: Upload PDF
- Drag and drop or browse to select your study material PDF
- System extracts text, chunks it, and builds the FAISS vector index
- Shows number of pages parsed and chunks created

### Step 2: Solve Doubts
- Type any question in the chat input
- Get document-grounded answers with `📄 Solved using Uploaded PDF (FAISS RAG)` badge
- Expand "Sources & Citations" to see exact page numbers

### Step 3: Personalize Profile (Optional)
- Set your difficulty level and learning style
- Provide weak and strong topics
- Future answers adapt to your preferences

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

- [LangChain](https://github.com/langchain-ai/langchain) & [LangGraph](https://github.com/langchain-ai/langgraph) — RAG framework and state-machine workflow orchestration
- [Groq](https://groq.com/) — Blazing-fast LLM inference API
- [Tavily](https://tavily.com/) — Web search API
- [FAISS](https://github.com/facebookresearch/faiss) by Meta AI — Efficient vector similarity search
- [HuggingFace](https://huggingface.co/) — BAAI/bge-small-en-v1.5 embedding model
- [Streamlit](https://streamlit.io/) — Python web application framework
- [FastAPI](https://fastapi.tiangolo.com/) — Modern, high-performance Python web framework
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF text extraction
