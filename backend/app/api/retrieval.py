from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval.retriever import RetrieverService
from app.services.retrieval.context_builder import ContextBuilder

router = APIRouter()

retriever = RetrieverService()


class RetrievalRequest(BaseModel):
    question: str


@router.post("/retrieve")
async def retrieve(request: RetrievalRequest):

    docs = retriever.retrieve(
        request.question
    )

    context = ContextBuilder.build(
        docs
    )

    return {

        "question": request.question,

        "documents_found": len(docs),

        "context": context
    }