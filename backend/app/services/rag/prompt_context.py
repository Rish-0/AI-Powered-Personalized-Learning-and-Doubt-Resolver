from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class PromptContext:

    question: str

    retrieved_context: str = ""

    conversation_memory: str = ""

    profile_context: str = ""

    web_context: str = ""

    sources: List = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)