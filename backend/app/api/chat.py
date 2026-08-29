from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag.rag_service import RAGService

router = APIRouter()


class ChatRequest(BaseModel):

    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    rag = RAGService()

    return rag.ask(request.question)