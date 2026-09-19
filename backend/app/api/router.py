from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

_manager = None


def _get_manager():
    global _manager
    if _manager is None:
        from app.services.agents.manager import AgentManager
        _manager = AgentManager()
    return _manager


class RouteRequest(BaseModel):

    question: str


@router.post("/route")

async def route_question(request: RouteRequest):

    return _get_manager().execute(
        request.question
    )