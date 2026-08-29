from fastapi import UploadFile

from app.services.file.file_service import FileService
from app.services.parser.pdf_parser import PDFParser
from app.services.chunking.text_chunker import TextChunker
from app.services.vectorstore.faiss_service import FAISSService


class IndexingService:

    def __init__(self):

        self.file_service = FileService()

        self.parser = PDFParser()

        self.chunker = TextChunker()

        self.vector_db = FAISSService()

    def index_pdf(self, file: UploadFile):

        saved = self.file_service.save_pdf(file)

        pages = self.parser.extract_text(
            saved["path"]
        )

        documents = self.chunker.chunk_pages(
            pages
        )

        db = self.vector_db.create(
            documents
        )

        self.vector_db.save(
            db
        )

        return {

            "message": "PDF indexed successfully",

            "pages": len(pages),

            "chunks": len(documents),

            "file": saved

        }