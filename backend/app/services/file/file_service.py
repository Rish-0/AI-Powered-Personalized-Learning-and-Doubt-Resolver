from pathlib import Path
import shutil
from fastapi import UploadFile, HTTPException

from app.core.constants import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE,
    UPLOAD_DIRECTORY,
)


class FileService:

    def save_pdf(self, file: UploadFile):

        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        if size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File exceeds 20 MB."
            )

        upload_path = Path(UPLOAD_DIRECTORY)
        upload_path.mkdir(exist_ok=True)

        destination = upload_path / file.filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "filename": file.filename,
            "path": str(destination)
        }