from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.indexing.indexing_service import IndexingService

router = APIRouter()

indexing_service = IndexingService()


@router.post("/upload")
async def upload_pdf(

    file: UploadFile = File(...)

):

    return indexing_service.index_pdf(file)