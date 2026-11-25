import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.graph.workflow import graph
from app.services.rag.rag_service import RAGService

router = APIRouter()


class ChatRequest(BaseModel):
    username: str = "student"
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    result = graph.invoke(
        {
            "username": request.username,
            "question": request.question,
            "route": "",
            "context": "",
            "answer": "",
            "sources": [],
            "memory": "",
            "profile": ""
        }
    )

    return {
        "question": result.get("question", request.question),
        "answer": result.get("answer", ""),
        "route": result.get("route", ""),
        "sources": result.get("sources", []),
        "fallback_from_pdf": result.get("route") == "WEB_SEARCH"
    }


@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    """
    Streams step-by-step progress events (e.g. searching PDF, searching Web with Tavily, synthesizing answer)
    followed by the final result JSON.
    """
    rag = RAGService()

    def generate_events():
        for event in rag.ask_stream(request.username, request.question):
            yield json.dumps(event) + "\n"

    return StreamingResponse(
        generate_events(),
        media_type="application/x-ndjson"
    )
