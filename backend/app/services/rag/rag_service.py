from app.services.retrieval.retriever import RetrieverService
from app.services.retrieval.context_builder import ContextBuilder
from app.services.routing.query_router import QueryRouter

from app.services.search.tavily_service import TavilyService
from app.services.rag.prompt_builder import PromptBuilder
from app.services.llm.groq_service import GroqService


class RAGService:

    def __init__(self):

        self.retriever = RetrieverService()

        self.groq = GroqService()

    def ask(self, question: str):

        web_query = QueryRouter.is_web_query(question)

        if web_query:

            results = TavilyService().search(question)
            docs = []
            context = ""

            for result in results:

                context += result["content"] + "\n\n"

        else:

            docs = self.retriever.retrieve(question)
            context = ContextBuilder.build(docs)

        prompt = PromptBuilder.build(question, context)
        answer = self.groq.chat(prompt)

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