from app.services.agents.router_agent import RouterAgent
from app.services.llm.groq_service import GroqService


# Lazy singletons — created on first use, not at import time
_router = None
_rag = None
_search = None
_groq = None


def _get_router():
    global _router
    if _router is None:
        _router = RouterAgent()
    return _router


def _get_rag():
    global _rag
    if _rag is None:
        from app.services.rag.rag_service import RAGService
        _rag = RAGService()
    return _rag


def _get_search():
    global _search
    if _search is None:
        from app.services.search.tavily_service import TavilyService
        _search = TavilyService()
    return _search


def _get_groq():
    global _groq
    if _groq is None:
        _groq = GroqService()
    return _groq


def router_node(state):

    route = _get_router().route(
        state["question"]
    )

    state["route"] = route

    return state


def pdf_node(state):

    result = _get_rag().ask(
        state.get("username", "student"),
        state["question"]
    )

    state["answer"] = result["answer"]

    state["sources"] = result["sources"]

    return state


def web_node(state):

    results = _get_search().search(
        state["question"]
    )

    context = ""

    for item in results:

        context += item["content"] + "\n"

    answer = _get_groq().generate_response(

        f"""
Use this context.

{context}

Question

{state['question']}

Answer
"""

    )

    state["answer"] = answer

    state["sources"] = results

    return state


def chat_node(state):

    state["answer"] = _get_groq().generate_response(

        state["question"]

    )

    state["sources"] = []

    return state