from pathlib import Path

from langchain_community.vectorstores import FAISS

from app.services.embeddings.embedding_service import EmbeddingService


class FAISSService:

    def __init__(self):

        self.embedding = EmbeddingService().get_embedding_model()

        self.index_path = Path("vector_store/faiss_index")

    def create(self, documents):

        return FAISS.from_documents(
            documents,
            self.embedding
        )

    def save(self, vector_store):

        self.index_path.mkdir(
            parents=True,
            exist_ok=True
        )

        vector_store.save_local(
            str(self.index_path)
        )

    def load(self):

        return FAISS.load_local(
            str(self.index_path),
            self.embedding,
            allow_dangerous_deserialization=True
        )