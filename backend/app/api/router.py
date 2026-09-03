from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agents.router_agent import RouterAgent
from app.services.agents.tool_executor import ToolExecutor

router = APIRouter()

agent = RouterAgent()

executor = ToolExecutor()


class RouteRequest(BaseModel):

    question: str


@router.post("/route")

async def route_question(

        request: RouteRequest

):

    route = agent.route(

        request.question

    )

    return executor.execute(

        route,

        request.question

    )