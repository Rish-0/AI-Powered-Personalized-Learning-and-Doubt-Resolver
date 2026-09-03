from app.services.agents.router_prompt import ROUTER_PROMPT
from app.services.llm.groq_service import GroqService


class RouterAgent:

    def __init__(self):

        self.llm = GroqService()

    def route(self, question: str):

        prompt = f"""

{ROUTER_PROMPT}

Question

{question}

Decision

"""

        decision = self.llm.generate_response(

            prompt

        )

        return decision.strip().upper()