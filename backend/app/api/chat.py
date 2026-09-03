from fastapi import APIRouter
from pydantic import BaseModel
from app.graph.workflow import graph

from app.services.rag.rag_service import RAGService

router = APIRouter()


class ChatRequest(BaseModel):

    question: str


@router.post("/chat")

async def chat(request: ChatRequest):

    result = graph.invoke(

        {

            "question": request.question,

            "route": "",

            "context": "",

            "answer": "",

            "sources": []

        }

    )

    return result