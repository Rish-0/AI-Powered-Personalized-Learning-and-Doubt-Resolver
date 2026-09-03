from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class PromptContext:

    question: str

    retrieved_context: str = ""

    conversation_memory: str = ""

    web_context: str = ""

    student_profile: Dict = field(default_factory=dict)

    sources: List = field(default_factory=list)