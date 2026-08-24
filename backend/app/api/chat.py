from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm.groq_service import GroqService

router = APIRouter()

groq_service = GroqService()


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    try:
        answer = groq_service.generate_response(request.question)

        return ChatResponse(answer=answer)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )