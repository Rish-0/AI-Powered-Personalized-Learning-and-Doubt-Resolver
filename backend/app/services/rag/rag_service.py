from app.services.retrieval.retriever import RetrieverService
from app.services.retrieval.context_builder import ContextBuilder

from app.services.rag.prompt_builder import PromptBuilder
from app.services.llm.groq_service import GroqService


class RAGService:

    def __init__(self):

        self.retriever = RetrieverService()

        self.groq = GroqService()

    def ask(self, question: str):

        docs = self.retriever.retrieve(question)

        context = ContextBuilder.build(docs)

        prompt = PromptBuilder.build(

            context,

            question

        )

        answer = self.groq.generate_response(

            prompt

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