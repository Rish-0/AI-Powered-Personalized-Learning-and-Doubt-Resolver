from fastapi import APIRouter
from pydantic import BaseModel

from app.graph.workflow import graph

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
        "sources": result.get("sources", [])
    }