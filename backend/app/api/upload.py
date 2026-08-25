from fastapi import APIRouter, UploadFile, File

from app.services.file.file_service import FileService
from app.services.parser.pdf_parser import PDFParser

router = APIRouter()

file_service = FileService()

pdf_parser = PDFParser()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    saved_file = file_service.save_pdf(file)

    pages = pdf_parser.extract_text(saved_file["path"])

    return {

        "message": "PDF uploaded successfully",

        "pages": len(pages),

        "preview": pages[:2],

        "file": saved_file

    }