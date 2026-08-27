from langchain_community.vectorstores import FAISS

from app.services.embeddings.embedding_service import EmbeddingService


class FAISSService:

    def __init__(self):

        self.embedding = EmbeddingService().get_model()

    def create_vector_store(self, chunks):

        vectorstore = FAISS.from_documents(

            documents=chunks,

            embedding=self.embedding

        )

        return vectorstore

    def save(self, vectorstore):

        vectorstore.save_local(

            "vector_store/faiss_index"
        )

    def load(self):

        return FAISS.load_local(

            "vector_store/faiss_index",

            self.embedding,

            allow_dangerous_deserialization=True

        )