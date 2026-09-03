from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.upload import router as upload_router
from app.api.retrieval import router as retrieval_router
from app.api.router import router as router_api  # <-- NEW

app = FastAPI(
    title="AI Tutor API",
    version="1.0.0"
)

# Existing routers
app.include_router(
    chat_router,
    prefix="/api",
    tags=["Chat"]
)

app.include_router(
    upload_router,
    prefix="/api",
    tags=["Upload"]
)

app.include_router(
    retrieval_router,
    prefix="/api",
    tags=["Retrieval"]
)

# NEW Router Agent API
app.include_router(
    router_api,
    prefix="/api",
    tags=["Router"]
)

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