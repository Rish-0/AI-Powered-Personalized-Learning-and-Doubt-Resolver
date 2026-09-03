from matplotlib.style import context

from app.services.retrieval.retriever import RetrieverService
from app.services.retrieval.context_builder import ContextBuilder
from app.services.rag.prompt_builder import PromptBuilder
from app.services.llm.groq_service import GroqService
from backend.app.services import memory
from backend.app.services.memory.conversation_service import ConversationService


class RAGService:

    def __init__(self):

        self.retriever = RetrieverService()

        self.groq = GroqService()

    def ask(self, question):

        docs = self.retriever.retrieve(question)

        context = ContextBuilder.build(docs)

        memory = ConversationService().get_recent_context()

        prompt_context = PromptContext(

            question=question,

            retrieved_context=context,

            conversation_memory=memory,

            sources=docs

        )

        prompt = PromptBuilder.build(
            prompt_context
        )

        answer = self.groq.generate_response(
            prompt
        )

        MemoryService().save(

            question,

            answer,

            "PDF_RAG"

        )

        return {

            "question": question,

            "answer": answer,

            "sources": [

                {

                    "page": doc.metadata["page"],

                    "source": doc.metadata["source"]

                }

                for doc in docs

            ]

        }