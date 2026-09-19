class ToolExecutor:

    def __init__(self):

        self._rag = None
        self._search = None
        self._llm = None

    @property
    def rag(self):
        if self._rag is None:
            from app.services.rag.rag_service import RAGService
            self._rag = RAGService()
        return self._rag

    @property
    def search(self):
        if self._search is None:
            from app.services.search.tavily_service import TavilyService
            self._search = TavilyService()
        return self._search

    @property
    def llm(self):
        if self._llm is None:
            from app.services.llm.groq_service import GroqService
            self._llm = GroqService()
        return self._llm

    def execute(self, route: str, question: str):

        route = route.upper()

        if route == "PDF_RAG":

            return self.rag.ask("student", question)

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