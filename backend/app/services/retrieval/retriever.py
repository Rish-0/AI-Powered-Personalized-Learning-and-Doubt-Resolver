from pathlib import Path
from app.services.vectorstore.faiss_service import FAISSService


class RetrieverService:

    def __init__(self):
        self.faiss = FAISSService()
        self.retriever = None
        self._last_mtime = 0
        self._try_load()

    def _try_load(self):
        """Try to load the FAISS index if it exists or if it has been updated."""
        try:
            if self.faiss.index_path.exists():
                index_file = self.faiss.index_path / "index.faiss"
                mtime = index_file.stat().st_mtime if index_file.exists() else 0
                if self.retriever is None or mtime != self._last_mtime:
                    vector_db = self.faiss.load()
                    self.retriever = vector_db.as_retriever(
                        search_type="similarity",
                        search_kwargs={"k": 6}
                    )
                    self._last_mtime = mtime
        except Exception:
            self.retriever = None

    def reload(self):
        """Force reload the index."""
        self.retriever = None
        self._try_load()

    def retrieve(self, question: str):
        self._try_load()

        if self.retriever is None:
            return []

        return self.retriever.invoke(question)
