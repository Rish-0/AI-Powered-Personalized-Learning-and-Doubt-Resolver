from typing import TypedDict
from typing import List


class GraphState(TypedDict):

    username: str

    question: str

    route: str

    profile: str

    memory: str

    context: str

    answer: str

    sources: List