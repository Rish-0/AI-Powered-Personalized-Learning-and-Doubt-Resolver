from pydantic import BaseModel
from typing import Optional


class AgentResponse(BaseModel):

    route: str

    answer: str

    sources: Optional[list] = None