from fastapi import FastAPI

from app.api.chat import router as chat_router

app = FastAPI(
    title="AI Tutor",
    version="1.0.0"
)

app.include_router(chat_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "AI Tutor API Running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }