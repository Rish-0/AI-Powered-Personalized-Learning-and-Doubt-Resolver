from pathlib import Path
import shutil
import uuid

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
                detail="Maximum file size is 20 MB."
            )

        upload_dir = Path(UPLOAD_DIRECTORY)

        upload_dir.mkdir(exist_ok=True)

        unique_name = f"{uuid.uuid4()}{extension}"

        destination = upload_dir / unique_name

        with destination.open("wb") as buffer:

            shutil.copyfileobj(file.file, buffer)

        return {

            "original_name": file.filename,

            "saved_name": unique_name,

            "path": str(destination)

        }