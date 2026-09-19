from fastapi import APIRouter

from app.services.memory.memory_service import MemoryService

router = APIRouter()

memory = MemoryService()


@router.get("/history")
async def get_history(limit: int = 20):

    rows = memory.history(limit=limit)

    return [
        {
            "id": row["id"],
            "question": row["question"],
            "answer": row["answer"],
            "route": row["route"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]
