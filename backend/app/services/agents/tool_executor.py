from app.services.rag.rag_service import RAGService
from app.services.search.tavily_service import TavilyService
from app.services.llm.groq_service import GroqService


class ToolExecutor:

    def __init__(self):

        self.rag = RAGService()

        self.search = TavilyService()

        self.llm = GroqService()

    def execute(self, route: str, question: str):

        route = route.upper()

        if route == "PDF_RAG":

            return self.rag.ask(question)

        elif route == "WEB_SEARCH":

            results = self.search.search(question)

            context = ""

            for result in results:

                context += f"""

Title:
{result.get("title")}

Content:
{result.get("content")}

"""

            prompt = f"""
Use the following search results.

{context}

Question

{question}

Answer:
"""

            answer = self.llm.generate_response(prompt)

            return {

            "answer":answer,

            "sources":results

            }

        else:

            answer = self.llm.generate_response(question)

            return {

                "route": "GENERAL_CHAT",

                "answer": answer

            }