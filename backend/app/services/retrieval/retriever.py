from app.services.vectorstore.faiss_service import FAISSService


class RetrieverService:

    def __init__(self):

        self.vector_db = FAISSService().load()

        self.retriever = self.vector_db.as_retriever(

            search_type="similarity",

            search_kwargs={
                "k": 5
            }

        )

    def retrieve(self, question: str):

        return self.retriever.invoke(question)