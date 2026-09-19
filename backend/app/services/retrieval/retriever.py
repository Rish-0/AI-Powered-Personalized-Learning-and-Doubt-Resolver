from pathlib import Path

from app.services.vectorstore.faiss_service import FAISSService


class RetrieverService:

    def __init__(self):

        self.faiss = FAISSService()

        self.retriever = None

        self._try_load()

    def _try_load(self):
        """Try to load the FAISS index. Silently skip if it doesn't exist yet."""
        try:
            if self.faiss.index_path.exists():
                vector_db = self.faiss.load()
                self.retriever = vector_db.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 5}
                )
        except Exception:
            self.retriever = None

    def reload(self):
        """Reload the index (call after a new PDF is uploaded)."""
        self._try_load()

    def retrieve(self, question):

        if self.retriever is None:
            self._try_load()

        if self.retriever is None:
            return []

        return self.retriever.invoke(question)