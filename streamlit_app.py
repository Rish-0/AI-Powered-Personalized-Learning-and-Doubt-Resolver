import os
import requests
import streamlit as st

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="AI Tutor — Personalized Learning & Doubt Resolver",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# Custom CSS for Modern, Guided Flow
# ==============================================================================
st.markdown(
    """
    <style>
    /* Global Background */
    .stApp {
        background: radial-gradient(circle at 10% 10%, rgba(108, 92, 231, 0.05) 0%, transparent 40%),
                    radial-gradient(circle at 90% 90%, rgba(0, 206, 201, 0.05) 0%, transparent 40%);
    }

    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, rgba(108, 92, 231, 0.12), rgba(0, 206, 201, 0.12));
        border: 1px solid rgba(108, 92, 231, 0.25);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(8px);
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6c5ce7, #00cec9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 6px 0;
    }
    .main-subtitle {
        color: #8f9ca8;
        font-size: 0.98rem;
        margin: 0;
    }

    /* Step Stepper Navigation */
    .stepper-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 24px;
        padding: 12px 18px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
    }
    .step-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.92rem;
        font-weight: 600;
        color: #888888;
    }
    .step-item.active {
        color: #00cec9;
    }
    .step-item.completed {
        color: #6c5ce7;
    }
    .step-circle {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        font-weight: 700;
        border: 2px solid #555555;
        color: #888888;
    }
    .step-circle.active {
        border-color: #00cec9;
        background: rgba(0, 206, 201, 0.15);
        color: #00cec9;
    }
    .step-circle.completed {
        border-color: #6c5ce7;
        background: rgba(108, 92, 231, 0.2);
        color: #a29bfe;
    }
    .step-arrow {
        color: #555555;
        font-size: 1.1rem;
    }

    /* Upload Hero Card */
    .upload-card {
        background: rgba(255, 255, 255, 0.02);
        border: 2px dashed rgba(108, 92, 231, 0.4);
        border-radius: 16px;
        padding: 32px 24px;
        text-align: center;
        margin-bottom: 24px;
        transition: all 0.2s ease;
    }
    .upload-card:hover {
        border-color: rgba(0, 206, 201, 0.6);
        background: rgba(108, 92, 231, 0.04);
    }
    .upload-icon {
        font-size: 3rem;
        margin-bottom: 12px;
    }

    /* Active Material Pill */
    .active-doc-banner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(108, 92, 231, 0.12);
        border: 1px solid rgba(108, 92, 231, 0.35);
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 18px;
    }
    .active-doc-text {
        font-size: 0.95rem;
        font-weight: 500;
        color: #dfe6e9;
    }

    /* Profile Nudge Card */
    .profile-nudge {
        background: linear-gradient(135deg, rgba(253, 203, 110, 0.1), rgba(225, 112, 85, 0.08));
        border: 1px solid rgba(253, 203, 110, 0.3);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 18px;
    }

    /* Route Badges */
    .route-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 6px 0;
    }
    .route-pdf {
        background: rgba(108, 92, 231, 0.18);
        color: #a29bfe;
        border: 1px solid rgba(108, 92, 231, 0.4);
    }
    .route-web {
        background: rgba(0, 206, 201, 0.18);
        color: #81ecec;
        border: 1px solid rgba(0, 206, 201, 0.4);
    }
    .route-general {
        background: rgba(9, 132, 227, 0.18);
        color: #74b9ff;
        border: 1px solid rgba(9, 132, 227, 0.4);
    }

    /* Source Box */
    .source-box {
        font-size: 0.85rem;
        padding: 6px 12px;
        margin: 4px 0;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.04);
        border-left: 3px solid #6c5ce7;
    }

    /* Status Pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 12px;
    }
    .status-online {
        background: rgba(46, 204, 113, 0.15);
        color: #2ecc71;
        border: 1px solid rgba(46, 204, 113, 0.3);
    }
    .status-offline {
        background: rgba(231, 76, 60, 0.15);
        color: #e74c3c;
        border: 1px solid rgba(231, 76, 60, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# Session State Initialization
# ==============================================================================
if "api_base" not in st.session_state:
    st.session_state.api_base = "http://localhost:8000"

if "username" not in st.session_state:
    st.session_state.username = "student"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tracks indexed PDF files and metadata: [{"name": str, "pages": int, "chunks": int}]
if "uploaded_files_cache" not in st.session_state:
    st.session_state.uploaded_files_cache = []

# Active document for reference
if "active_document" not in st.session_state:
    st.session_state.active_document = None

# Tracks whether user has personalized profile
if "profile_created" not in st.session_state:
    st.session_state.profile_created = False

if "profile_data" not in st.session_state:
    st.session_state.profile_data = {
        "difficulty": "medium",
        "learning_style": "textual",
        "weak_topics": "",
        "strong_topics": "",
    }

# Tracks if profile drawer should be open
if "show_profile_form" not in st.session_state:
    st.session_state.show_profile_form = False

# Starter prompt carrier
if "starter_prompt" not in st.session_state:
    st.session_state.starter_prompt = None

# ==============================================================================
# API Helper Functions
# ==============================================================================
def check_health():
    try:
        r = requests.get(f"{st.session_state.api_base}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def get_profile(username: str):
    try:
        r = requests.get(f"{st.session_state.api_base}/api/profile/{username}", timeout=3)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def save_profile(username: str, difficulty: str, learning_style: str, weak_topics: str, strong_topics: str):
    payload = {
        "username": username,
        "difficulty": difficulty,
        "learning_style": learning_style,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
    }
    try:
        r = requests.post(f"{st.session_state.api_base}/api/profile", json=payload, timeout=4)
        return r.status_code == 200
    except Exception:
        return False


def get_history(limit: int = 15):
    try:
        r = requests.get(f"{st.session_state.api_base}/api/history?limit={limit}", timeout=3)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []


def upload_pdf_file(file):
    try:
        files = {"file": (file.name, file.getvalue(), "application/pdf")}
        r = requests.post(f"{st.session_state.api_base}/api/upload", files=files, timeout=60)
        if r.status_code == 200:
            return True, r.json()
        return False, f"Server responded with status code {r.status_code}: {r.text}"
    except Exception as e:
        return False, str(e)


def send_chat_message(username: str, question: str):
    try:
        payload = {"username": username, "question": question}
        r = requests.post(f"{st.session_state.api_base}/api/chat", json=payload, timeout=60)
        if r.status_code == 200:
            return True, r.json()
        return False, f"Server Error ({r.status_code}): {r.text}"
    except Exception as e:
        return False, str(e)


def render_route_badge(route: str):
    if not route:
        return ""
    route_upper = route.upper()
    if route_upper == "PDF_RAG":
        return '<div class="route-badge route-pdf">📄 Solved using Uploaded PDF (FAISS RAG)</div>'
    elif route_upper == "WEB_SEARCH":
        return '<div class="route-badge route-web">🌐 Solved using Tavily Web Search (Not found in PDF)</div>'
    elif route_upper == "GENERAL_CHAT":
        return '<div class="route-badge route-general">💬 Solved using General Knowledge</div>'
    return f'<div class="route-badge route-general">{route}</div>'


def send_chat_message_stream(username: str, question: str):
    """
    Streams step-by-step progress events (e.g. searching PDF, searching Web with Tavily)
    from the backend /api/chat/stream endpoint.
    Falls back to /api/chat if streaming is unavailable.
    """
    import json
    try:
        payload = {"username": username, "question": question}
        r = requests.post(f"{st.session_state.api_base}/api/chat/stream", json=payload, stream=True, timeout=90)
        if r.status_code == 200:
            for line in r.iter_lines():
                if line:
                    event = json.loads(line.decode("utf-8"))
                    yield True, event
            return
    except Exception:
        pass

    # Fallback to standard endpoint
    success, res = send_chat_message(username, question)
    if success:
        yield True, {"step": "done", "data": res}
    else:
        yield False, {"error": str(res)}


# ==============================================================================
# Sidebar
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎓 AI Doubt Resolver")

    # Health check
    if check_health():
        st.markdown(
            '<div class="status-pill status-online">🟢 Backend Connected</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-pill status-offline">🔴 Backend Offline</div>',
            unsafe_allow_html=True,
        )
        st.caption("Backend should run on `http://localhost:8000`.")

    st.divider()

    # Current Status Overview
    st.markdown("#### 📌 Current Workflow")
    has_pdf = len(st.session_state.uploaded_files_cache) > 0
    doubts_count = len([m for m in st.session_state.messages if m["role"] == "user"])

    if has_pdf:
        st.markdown(f"✅ **PDF Material:** `{st.session_state.active_document or st.session_state.uploaded_files_cache[0]['name']}`")
    else:
        st.markdown("⏳ **Step 1:** Upload PDF required")

    st.markdown(f"💬 **Doubts Solved:** {doubts_count}")

    if st.session_state.profile_created:
        st.markdown(f"👤 **Profile:** `{st.session_state.username}` ({st.session_state.profile_data['difficulty'].capitalize()})")
    else:
        st.markdown("⚙️ **Profile:** Default *(Click below to personalize)*")

    st.divider()

    # Uploaded Materials list
    if has_pdf:
        with st.expander("📚 Uploaded Study Materials", expanded=True):
            for f in st.session_state.uploaded_files_cache:
                st.markdown(f"- 📄 **{f['name']}** ({f['pages']} pages, {f['chunks']} chunks)")

            if st.button("➕ Upload Another PDF", use_container_width=True):
                st.session_state.force_upload_view = True
                st.rerun()

    # History
    with st.expander("🕒 Past Doubts & History", expanded=False):
        history_items = get_history(limit=8)
        if history_items:
            for item in history_items:
                route = item.get("route", "")
                icon = "📄" if route == "PDF_RAG" else ("🌐" if route == "WEB_SEARCH" else "💬")
                q_text = item.get("question", "")
                if st.button(f"{icon} {q_text[:30]}...", key=f"hist_{item.get('id')}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": item["question"]})
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": item["answer"],
                            "route": item.get("route"),
                            "sources": [],
                        }
                    )
                    st.rerun()
        else:
            st.caption("No past questions logged.")

    st.divider()

    # Reset / New Session
    if st.button("✨ New Session / Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ==============================================================================
# Main Content Area
# ==============================================================================

# Header
st.markdown(
    """
    <div class="main-header">
        <h1 class="main-title">🎓 AI-Powered Study Doubt Resolver</h1>
        <p class="main-subtitle">
            Upload your PDF study material first, ask any doubt to get context-grounded answers with citations, 
            and create your personalized learning profile to adapt explanations to your style.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Flow Progression Stepper Bar
has_uploaded = len(st.session_state.uploaded_files_cache) > 0
has_solved_doubts = len(st.session_state.messages) > 0

step1_class = "completed" if has_uploaded else "active"
step2_class = "active" if has_uploaded and not st.session_state.profile_created else ("completed" if has_solved_doubts else "")
step3_class = "completed" if st.session_state.profile_created else ("active" if has_solved_doubts else "")

st.markdown(
    f"""
    <div class="stepper-container">
        <div class="step-item {step1_class}">
            <div class="step-circle {step1_class}">1</div>
            <span>Upload PDF</span>
        </div>
        <span class="step-arrow">➔</span>
        <div class="step-item {step2_class}">
            <div class="step-circle {step2_class}">2</div>
            <span>Solve Doubts</span>
        </div>
        <span class="step-arrow">➔</span>
        <div class="step-item {step3_class}">
            <div class="step-circle {step3_class}">3</div>
            <span>Personalize Profile</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# STEP 1: Upload PDF (Mandatory First Step)
# ==============================================================================
force_upload = st.session_state.get("force_upload_view", False)

if not has_uploaded or force_upload:
    st.markdown("### 📄 Step 1: Upload Your Study Material (PDF)")
    st.markdown(
        "Please upload the textbook, lecture slides, or study notes (PDF) you want help with. "
        "The system will index it into the vector database so you can ask any doubts directly from it."
    )

    upload_col1, upload_col2 = st.columns([2, 1])

    with upload_col1:
        uploaded_file = st.file_uploader(
            "Choose a PDF file to index",
            type=["pdf"],
            help="Maximum file size: 20 MB",
            key="primary_pdf_uploader",
        )

        if uploaded_file is not None:
            st.info(f"Selected file: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
            if st.button("🚀 Upload & Index PDF into Vector Store", type="primary", use_container_width=True):
                with st.spinner("Extracting text, chunking, and embedding with FAISS..."):
                    success, res = upload_pdf_file(uploaded_file)
                    if success:
                        pages = res.get("pages", 0)
                        chunks = res.get("chunks", 0)
                        doc_info = {"name": uploaded_file.name, "pages": pages, "chunks": chunks}
                        st.session_state.uploaded_files_cache.append(doc_info)
                        st.session_state.active_document = uploaded_file.name
                        st.session_state.force_upload_view = False
                        st.success(f"🎉 **{uploaded_file.name}** successfully indexed! ({pages} pages, {chunks} chunks)")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to index PDF: {res}")

    with upload_col2:
        st.markdown("#### 💡 What happens next?")
        st.markdown(
            """
            1. **Chunking & Indexing:** Your PDF is converted into semantic vector embeddings.
            2. **Direct Doubt Resolution:** You can ask questions, ask for summaries, or clarify difficult topics.
            3. **Personalization Option:** Tailor future explanations to your learning style (Visual, Textual, Step-by-Step) and difficulty!
            """
        )
        if has_uploaded and force_upload:
            if st.button("Back to Chat ➔"):
                st.session_state.force_upload_view = False
                st.rerun()

    # If no PDF is uploaded yet, stop here so user completes Step 1 first
    if not has_uploaded:
        st.stop()


# ==============================================================================
# Active Document Banner
# ==============================================================================
active_doc = st.session_state.active_document or st.session_state.uploaded_files_cache[-1]["name"]
doc_meta = next((f for f in st.session_state.uploaded_files_cache if f["name"] == active_doc), None)
pages_count = doc_meta["pages"] if doc_meta else "N/A"
chunks_count = doc_meta["chunks"] if doc_meta else "N/A"

col_banner, col_switch = st.columns([4, 1])
with col_banner:
    st.markdown(
        f"""
        <div class="active-doc-banner">
            <span class="active-doc-text">
                📖 <b>Active Document:</b> <code>{active_doc}</code> &nbsp; | &nbsp; 
                📄 <b>Pages:</b> {pages_count} &nbsp; | &nbsp; 
                🧩 <b>Chunks:</b> {chunks_count}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_switch:
    if st.button("🔄 Change PDF", use_container_width=True):
        st.session_state.force_upload_view = True
        st.rerun()


# ==============================================================================
# STEP 3 OPTION: Student Profile Personalization Card / Expander
# ==============================================================================
# Offer the option to create/customize profile prominently
profile_expander_title = (
    f"👤 Student Profile: {st.session_state.username} ({st.session_state.profile_data['difficulty'].capitalize()}) — Click to Edit"
    if st.session_state.profile_created
    else "✨ Option: Create / Personalize Your Learning Profile (Click to set difficulty & style)"
)

with st.expander(profile_expander_title, expanded=st.session_state.show_profile_form):
    st.markdown(
        "Customize your learning profile so the AI adapts its explanations specifically to your preferred style and difficulty:"
    )

    p_col1, p_col2 = st.columns(2)

    with p_col1:
        u_name = st.text_input("Username", value=st.session_state.username, key="prof_username")

        diff_map = {"Beginner 🌱 (Simple fundamentals)": "beginner", "Intermediate 📖 (Standard academic)": "medium", "Advanced 🚀 (Deep dive & technical)": "advanced"}
        diff_keys = list(diff_map.keys())
        current_diff = st.session_state.profile_data.get("difficulty", "medium")
        diff_idx = 1
        for i, (k, v) in enumerate(diff_map.items()):
            if v == current_diff:
                diff_idx = i
                break
        selected_diff = st.selectbox("Difficulty Level", diff_keys, index=diff_idx)

        style_map = {
            "Textual 📝 (Detailed, thorough explanations)": "textual",
            "Visual 👁️ (Structured breakdown, diagrams, mental models)": "visual",
            "Example-based 💡 (Concrete real-world examples & analogies)": "example-based",
            "Step-by-step 🪜 (Sequential, numbered walkthrough)": "step-by-step",
        }
        style_keys = list(style_map.keys())
        current_style = st.session_state.profile_data.get("learning_style", "textual")
        style_idx = 0
        for i, (k, v) in enumerate(style_map.items()):
            if v == current_style:
                style_idx = i
                break
        selected_style = st.selectbox("Learning Style", style_keys, index=style_idx)

    with p_col2:
        weak_topics = st.text_input(
            "Weak Topics (AI will provide extra guidance here)",
            value=st.session_state.profile_data.get("weak_topics", ""),
            placeholder="e.g. Memory Management, Dynamic Programming, Proofs",
        )
        strong_topics = st.text_input(
            "Strong Topics (AI won't waste time on basic definitions)",
            value=st.session_state.profile_data.get("strong_topics", ""),
            placeholder="e.g. Python, File I/O, Basic Arrays",
        )

        st.write("")
        if st.button("💾 Save & Apply Profile", type="primary", use_container_width=True):
            chosen_diff = diff_map[selected_diff]
            chosen_style = style_map[selected_style]
            st.session_state.username = u_name.strip() or "student"
            st.session_state.profile_data = {
                "difficulty": chosen_diff,
                "learning_style": chosen_style,
                "weak_topics": weak_topics,
                "strong_topics": strong_topics,
            }
            save_profile(st.session_state.username, chosen_diff, chosen_style, weak_topics, strong_topics)
            st.session_state.profile_created = True
            st.session_state.show_profile_form = False
            st.success(f"Profile saved! Answers will now be tailored to: **{chosen_diff.capitalize()}** level with **{chosen_style}** style.")
            st.rerun()


# ==============================================================================
# STEP 2: Solve Doubts (Chat Interface)
# ==============================================================================
st.markdown("### 💬 Step 2: Ask Your Doubt")

# If chat is empty, show helpful starter suggestions tailored to the uploaded material
if not st.session_state.messages:
    st.markdown("##### 💡 Suggested questions from your uploaded document:")
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        if st.button(f"📑 Summarize key concepts from {active_doc}", use_container_width=True):
            st.session_state.starter_prompt = f"Summarize the key concepts and important formulas/topics covered in {active_doc}"
        if st.button("❓ What are the most important exam questions from this material?", use_container_width=True):
            st.session_state.starter_prompt = "What are the most important potential exam questions and key points from this document?"

    with col_s2:
        if st.button("🧠 Explain the most complex topic in this document simply", use_container_width=True):
            st.session_state.starter_prompt = "Find and explain the most complex or difficult topic in this document in a simple, easy-to-understand way"
        if st.button("📝 Generate 3 practice problems with solutions based on this PDF", use_container_width=True):
            st.session_state.starter_prompt = "Generate 3 conceptual practice problems with step-by-step solutions based on this PDF"


# Render conversation
for idx, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🎓"):
            # Route badge
            route = msg.get("route")
            if route:
                st.markdown(render_route_badge(route), unsafe_allow_html=True)

            if route == "WEB_SEARCH":
                st.info("🌐 **Web Search Fallback:** This doubt was not found in your uploaded study material, so real-time information was retrieved from the web via Tavily.")

            # Response content
            st.markdown(msg["content"])

            # Sources / Citations from PDF or Web
            sources = msg.get("sources") or []
            if sources:
                with st.expander(f"📚 View Citations & Sources ({len(sources)})", expanded=False):
                    if route == "PDF_RAG":
                        for s in sources:
                            doc_title = s.get("source", active_doc)
                            page_no = s.get("page", "N/A")
                            st.markdown(f'<div class="source-box">📄 <b>{doc_title}</b> — Page {page_no}</div>', unsafe_allow_html=True)
                    elif route == "WEB_SEARCH":
                        for s in sources:
                            title = s.get("title") or s.get("url") or "Web Result"
                            url = s.get("url", "#")
                            snippet = s.get("snippet", "")
                            snippet_html = f'<br><small style="color: #a0aec0;">{snippet}</small>' if snippet else ""
                            st.markdown(f'<div class="source-box">🌐 <a href="{url}" target="_blank"><b>{title}</b></a>{snippet_html}</div>', unsafe_allow_html=True)
                    else:
                        st.json(sources)


# Nudge to create profile if doubts have been asked but profile is not created yet
if has_solved_doubts and not st.session_state.profile_created and not st.session_state.show_profile_form:
    st.markdown(
        """
        <div class="profile-nudge">
            🌟 <b>Want these answers tailored to you?</b> 
            You can set your difficulty (Beginner/Advanced) and learning style (Step-by-step, Visual, or Example-based).
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("👤 Set Up Learning Profile Now"):
        st.session_state.show_profile_form = True
        st.rerun()


# Pending prompt from suggestions
prompt_to_send = None
if st.session_state.starter_prompt:
    prompt_to_send = st.session_state.starter_prompt
    st.session_state.starter_prompt = None

# Chat Input
user_input = st.chat_input("Type your doubt here (e.g. 'Explain section 2', 'What is X in page 5?')...")
final_prompt = prompt_to_send or user_input

if final_prompt:
    # 1. Append user message
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(final_prompt)

    # 2. Get answer from backend with real-time status loader
    with st.chat_message("assistant", avatar="🎓"):
        status_box = st.status("🔍 Searching uploaded PDF...", expanded=True)
        res = None
        final_error = None

        for ok, event in send_chat_message_stream(st.session_state.username, final_prompt):
            if not ok:
                final_error = event.get("error", "Failed to connect to backend.")
                break

            step = event.get("step")
            msg_text = event.get("message", "")

            if step == "searching_pdf":
                status_box.update(label="🔍 Searching uploaded PDF for answers...", state="running")
                status_box.write(msg_text)
            elif step == "analyzing_pdf":
                status_box.update(label="📄 Analyzing document excerpts with AI...", state="running")
                status_box.write(msg_text)
            elif step == "searching_web":
                status_box.update(label="🌐 Question not found in PDF. Searching the web with Tavily...", state="running")
                status_box.write("⚠️ **Topic not found in uploaded PDF.** Launching live **Tavily Web Search**...")
            elif step == "done":
                res = event.get("data", {})
                route = res.get("route", "")
                if route == "WEB_SEARCH":
                    status_box.update(label="🌐 Solved via Tavily Web Search (Not found in PDF)", state="complete", expanded=False)
                else:
                    status_box.update(label="📄 Solved from Uploaded PDF", state="complete", expanded=False)

        if res:
            answer = res.get("answer", "No answer could be generated.")
            route = res.get("route", "")
            sources = res.get("sources", [])

            if route:
                st.markdown(render_route_badge(route), unsafe_allow_html=True)

            if route == "WEB_SEARCH":
                st.info("🌐 **Web Search Fallback:** This doubt was not found in your uploaded study material, so real-time information was retrieved from the web via Tavily.")

            st.markdown(answer)

            if sources:
                with st.expander(f"📚 View Citations & Sources ({len(sources)})", expanded=False):
                    if route == "PDF_RAG":
                        for s in sources:
                            doc_title = s.get("source", active_doc)
                            page_no = s.get("page", "N/A")
                            st.markdown(f'<div class="source-box">📄 <b>{doc_title}</b> — Page {page_no}</div>', unsafe_allow_html=True)
                    elif route == "WEB_SEARCH":
                        for s in sources:
                            title = s.get("title") or s.get("url") or "Web Result"
                            url = s.get("url", "#")
                            snippet = s.get("snippet", "")
                            snippet_html = f'<br><small style="color: #a0aec0;">{snippet}</small>' if snippet else ""
                            st.markdown(f'<div class="source-box">🌐 <a href="{url}" target="_blank"><b>{title}</b></a>{snippet_html}</div>', unsafe_allow_html=True)
                    else:
                        st.json(sources)

            # Store assistant response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "route": route,
                    "sources": sources,
                }
            )
        elif final_error:
            status_box.update(label="❌ Failed to solve doubt", state="error", expanded=True)
            error_msg = f"⚠️ Could not solve doubt.\n\n**Details:** {final_error}\n\nPlease check backend connection at `{st.session_state.api_base}`."
            st.error(error_msg)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_msg,
                    "route": "ERROR",
                    "sources": [],
                }
            )

    st.rerun()
