from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agents.manager import AgentManager

router = APIRouter()

manager = AgentManager()


class RouteRequest(BaseModel):

    question: str


@router.post("/route")

async def route_question(request: RouteRequest):

    return manager.execute(
        request.question
    )