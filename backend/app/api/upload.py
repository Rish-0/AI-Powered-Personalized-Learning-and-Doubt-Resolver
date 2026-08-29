from fastapi import APIRouter, UploadFile, File

from app.services.indexing.indexing_service import IndexingService

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    indexing_service = IndexingService()

    return indexing_service.index_pdf(file)