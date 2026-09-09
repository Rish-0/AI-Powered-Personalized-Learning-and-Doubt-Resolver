from dataclasses import dataclass, field
from typing import Any


@dataclass
class PromptContext:
    """
    Central object passed to PromptBuilder.

    Every new feature (memory, profile, web search,
    recommendations, quiz history, etc.) will simply
    populate this object.
    """

    # Current question
    question: str

    # Retrieved from FAISS
    retrieved_context: str = ""

    # Previous conversation
    conversation_memory: str = ""

    # Student profile
    profile_context: str = ""

    # Internet search results
    web_context: str = ""

    # References returned by retriever
    sources: list = field(default_factory=list)

    # Extra metadata
    metadata: dict[str, Any] = field(default_factory=dict)