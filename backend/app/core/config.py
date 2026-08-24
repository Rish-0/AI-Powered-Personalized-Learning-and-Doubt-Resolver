from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

class Settings:
    APP_NAME = "AI Tutor"
    VERSION = "1.0.0"
    MODEL_NAME = os.getenv("MODEL_NAME")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Add it to backend/app/.env "
            "or set it as an environment variable."
        )

settings = Settings()