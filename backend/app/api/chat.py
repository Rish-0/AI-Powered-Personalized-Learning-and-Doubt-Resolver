from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag.rag_service import RAGService

router = APIRouter()

rag = RAGService()


class ChatRequest(BaseModel):

    question: str


@router.post("/chat")

async def chat(

        request: ChatRequest

):

    return rag.ask(

        request.question

    )