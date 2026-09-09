from app.services.retrieval.retriever import RetrieverService
from app.services.retrieval.context_builder import ContextBuilder

from app.services.rag.prompt_context import PromptContext
from app.services.rag.prompt_builder import PromptBuilder

from app.services.llm.groq_service import GroqService

from app.services.memory.memory_service import MemoryService
from app.services.memory.conversation_service import ConversationService

from app.services.personalization.personalization_service import (
    PersonalizationService,
)


class RAGService:

    def __init__(self):

        self.retriever = RetrieverService()

        self.groq = GroqService()

        self.memory = MemoryService()

        self.conversation = ConversationService()

        self.personalization = PersonalizationService()

    def ask(self, username: str, question: str):

        documents = self.retriever.retrieve(question)

        retrieved_context = ContextBuilder.build(
            documents
        )

        conversation_memory = (
            self.conversation.get_recent_context()
        )

        profile = (
            self.personalization.build_profile_context(
                username
            )
        )

        prompt_context = PromptContext(

            question=question,

            retrieved_context=retrieved_context,

            conversation_memory=conversation_memory,

            profile_context=profile,

            sources=documents

        )

        prompt = PromptBuilder.build(
            prompt_context
        )

        answer = self.groq.generate_response(
            prompt
        )

        self.memory.save(

            question,

            answer,

            "PDF_RAG"

        )

        return {

            "question": question,

            "answer": answer,

            "sources": [

                {

                    "page": doc.metadata.get("page"),

                    "source": doc.metadata.get("source")

                }

                for doc in documents

            ]

        }