from fastapi import APIRouter, UploadFile, File

from app.services.file.file_service import FileService
from app.services.parser.pdf_parser import PDFParser
from app.services.chunking.text_chunker import TextChunker

router = APIRouter()

file_service = FileService()

pdf_parser = PDFParser()

chunker = TextChunker()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    saved_file = file_service.save_pdf(file)

    pages = pdf_parser.extract_text(
        saved_file["path"]
    )

    chunks = chunker.chunk_pages(pages)

    return {

        "message": "PDF processed successfully",

        "pages": len(pages),

        "chunks": len(chunks),

        "preview": chunks[:3],

        "file": saved_file

    }