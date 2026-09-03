from app.services.agents.router_agent import RouterAgent
from app.services.agents.tool_executor import ToolExecutor


class AgentManager:

    def __init__(self):

        self.router = RouterAgent()

        self.executor = ToolExecutor()

    def execute(self, question: str):

        route = self.router.route(question)

        result = self.executor.execute(
            route,
            question
        )

        return {

            "route": route,

            **result

        }