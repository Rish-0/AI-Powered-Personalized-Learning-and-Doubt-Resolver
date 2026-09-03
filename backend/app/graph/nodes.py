from app.services.agents.router_agent import RouterAgent
from app.services.rag.rag_service import RAGService
from app.services.search.tavily_service import TavilyService
from app.services.llm.groq_service import GroqService


router = RouterAgent()

rag = RAGService()

search = TavilyService()

groq = GroqService()


def router_node(state):

    route = router.route(
        state["question"]
    )

    state["route"] = route

    return state


def pdf_node(state):

    result = rag.ask(
        state["question"]
    )

    state["answer"] = result["answer"]

    state["sources"] = result["sources"]

    return state


def web_node(state):

    results = search.search(
        state["question"]
    )

    context = ""

    for item in results:

        context += item["content"] + "\n"

    answer = groq.generate_response(

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

    state["answer"] = groq.generate_response(

        state["question"]

    )

    state["sources"] = []

    return state