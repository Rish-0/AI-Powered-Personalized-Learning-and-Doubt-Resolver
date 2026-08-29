from app.services.vectorstore.faiss_service import FAISSService


class RetrieverService:

    def __init__(self):

        vector_db = FAISSService().load()

        self.retriever = vector_db.as_retriever(

            search_type="similarity",

            search_kwargs={"k": 5}

        )

    def retrieve(self, question):

        return self.retriever.invoke(question)