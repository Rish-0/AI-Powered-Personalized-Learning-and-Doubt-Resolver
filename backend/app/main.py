from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.upload import router as upload_router

app = FastAPI(
    title="AI Tutor",
    version="1.0.0"
)

app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(upload_router, prefix="/api", tags=["Upload"])


@app.get("/")
async def root():
    return {"message": "AI Tutor API Running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}