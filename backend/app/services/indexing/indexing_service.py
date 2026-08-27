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

        # Save uploaded file
        saved_file = self.file_service.save_pdf(file)

        # Parse PDF
        pages = self.parser.extract_text(
            saved_file["path"]
        )

        # Chunk pages
        documents = self.chunker.chunk_pages(
            pages
        )

        # Build Vector Store
        db = self.vector_db.create(
            documents
        )

        # Save Vector Store
        self.vector_db.save(db)

        return {

            "message": "PDF indexed successfully",

            "file": saved_file,

            "pages": len(pages),

            "chunks": len(documents)

        }