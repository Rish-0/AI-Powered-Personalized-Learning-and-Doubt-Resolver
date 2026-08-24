from fastapi import APIRouter, UploadFile, File

from app.services.file.file_service import FileService

router = APIRouter()

file_service = FileService()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    result = file_service.save_pdf(file)

    return {
        "message": "File uploaded successfully",
        "data": result
    }