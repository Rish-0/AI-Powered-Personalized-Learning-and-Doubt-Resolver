from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agents.router_agent import RouterAgent

router = APIRouter()

agent = RouterAgent()


class RouteRequest(BaseModel):

    question: str


@router.post("/route")

async def route_question(

        request: RouteRequest

):

    decision = agent.route(

        request.question

    )

    return {

        "question": request.question,

        "route": decision

    }