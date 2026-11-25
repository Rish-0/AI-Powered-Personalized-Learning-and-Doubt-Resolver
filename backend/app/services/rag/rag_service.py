from app.services.retrieval.retriever import RetrieverService
from app.services.retrieval.context_builder import ContextBuilder
from app.services.rag.prompt_context import PromptContext
from app.services.rag.prompt_builder import PromptBuilder
from app.services.llm.groq_service import GroqService
from app.services.search.tavily_service import TavilyService
from app.services.memory.memory_service import MemoryService
from app.services.memory.conversation_service import ConversationService
from app.services.personalization.personalization_service import (
    PersonalizationService,
)


class RAGService:

    def __init__(self):
        self.retriever = RetrieverService()
        self.groq = GroqService()
        self.search = TavilyService()
        self.memory = MemoryService()
        self.conversation = ConversationService()
        self.personalization = PersonalizationService()

    def _is_not_found(self, text: str) -> bool:
        if not text:
            return True
        clean = text.strip().upper()
        if clean.startswith("NOT_FOUND_IN_PDF") or "NOT_FOUND_IN_PDF" in clean:
            return True
        lower = text.lower()
        triggers = [
            "could not find the answer in the uploaded document",
            "couldn't find the answer in the uploaded document",
            "does not contain information",
            "not mentioned in the provided pdf",
            "not covered in the uploaded document",
        ]
        return any(t in lower for t in triggers)

    def _execute_web_search(self, username: str, question: str):
        web_results = self.search.search(question)

        web_context = ""
        sources = []
        for item in web_results:
            title = item.get("title", "Web Result")
            url = item.get("url", "#")
            content = item.get("content", "")
            web_context += f"Source: {title}\nURL: {url}\nExcerpt: {content}\n\n"
            sources.append({
                "title": title,
                "url": url,
                "snippet": content[:250] if content else ""
            })

        profile = self.personalization.build_profile_context(username)
        conversation_memory = self.conversation.get_recent_context()

        if web_context.strip():
            prompt = PromptBuilder.build_web_prompt(
                question=question,
                web_context=web_context,
                profile_context=profile,
                conversation_memory=conversation_memory,
            )
            answer = self.groq.generate_response(prompt)
        else:
            # Fallback to general LLM response if web search returned no results
            fallback_prompt = (
                f"You are an AI Tutor. Answer the student's question accurately and helpfully.\n\n"
                f"Student Profile:\n{profile}\n\n"
                f"Question:\n{question}\n\nAnswer:"
            )
            answer = self.groq.generate_response(fallback_prompt)

        self.memory.save(question, answer, "WEB_SEARCH")

        return {
            "question": question,
            "answer": answer,
            "route": "WEB_SEARCH",
            "sources": sources,
            "fallback_from_pdf": True,
        }

    def ask(self, username: str, question: str):
        documents = self.retriever.retrieve(question)

        retrieved_context = ContextBuilder.build(documents) if documents else ""

        # If no documents or empty context, directly fall back to Tavily web search
        if not documents or not retrieved_context.strip():
            return self._execute_web_search(username, question)

        conversation_memory = self.conversation.get_recent_context()
        profile = self.personalization.build_profile_context(username)

        prompt_context = PromptContext(
            question=question,
            retrieved_context=retrieved_context,
            conversation_memory=conversation_memory,
            profile_context=profile,
            sources=documents,
        )

        prompt = PromptBuilder.build(prompt_context)
        answer = self.groq.generate_response(prompt)

        # If LLM reports question is not found in the uploaded PDF, trigger Tavily web search
        if self._is_not_found(answer):
            return self._execute_web_search(username, question)

        # Found in PDF
        self.memory.save(question, answer, "PDF_RAG")

        return {
            "question": question,
            "answer": answer,
            "route": "PDF_RAG",
            "sources": [
                {
                    "page": doc.metadata.get("page"),
                    "source": doc.metadata.get("source"),
                }
                for doc in documents
            ],
            "fallback_from_pdf": False,
        }

    def ask_stream(self, username: str, question: str):
        """
        Generator yielding step-by-step progress events for the frontend loader,
        then the final result.
        """
        yield {
            "step": "searching_pdf",
            "message": "🔍 Searching uploaded PDF for relevant sections...",
        }

        documents = self.retriever.retrieve(question)
        retrieved_context = ContextBuilder.build(documents) if documents else ""

        if not documents or not retrieved_context.strip():
            yield {
                "step": "searching_web",
                "message": "🌐 Not found in PDF. Searching the web with Tavily...",
            }
            res = self._execute_web_search(username, question)
            yield {
                "step": "done",
                "message": "Answer synthesized via Tavily Web Search.",
                "data": res,
            }
            return

        yield {
            "step": "analyzing_pdf",
            "message": "📄 Analyzing document excerpts with AI...",
        }

        conversation_memory = self.conversation.get_recent_context()
        profile = self.personalization.build_profile_context(username)

        prompt_context = PromptContext(
            question=question,
            retrieved_context=retrieved_context,
            conversation_memory=conversation_memory,
            profile_context=profile,
            sources=documents,
        )

        prompt = PromptBuilder.build(prompt_context)
        answer = self.groq.generate_response(prompt)

        if self._is_not_found(answer):
            yield {
                "step": "searching_web",
                "message": "🌐 Not found in PDF. Searching the web with Tavily...",
            }
            res = self._execute_web_search(username, question)
            yield {
                "step": "done",
                "message": "Answer synthesized via Tavily Web Search.",
                "data": res,
            }
            return

        # Found in PDF
        self.memory.save(question, answer, "PDF_RAG")
        pdf_res = {
            "question": question,
            "answer": answer,
            "route": "PDF_RAG",
            "sources": [
                {
                    "page": doc.metadata.get("page"),
                    "source": doc.metadata.get("source"),
                }
                for doc in documents
            ],
            "fallback_from_pdf": False,
        }
        yield {
            "step": "done",
            "message": "Answer synthesized from uploaded PDF.",
            "data": pdf_res,
        }
