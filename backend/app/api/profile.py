from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.services.profile.profile_service import ProfileService

router = APIRouter()

profile = ProfileService()


class ProfileUpdateRequest(BaseModel):
    username: str
    difficulty: Optional[str] = None
    learning_style: Optional[str] = None
    weak_topics: Optional[str] = None
    strong_topics: Optional[str] = None


@router.get("/profile/{username}")
async def get_profile(username: str):
    return profile.get_profile(username)


@router.post("/profile")
async def update_profile(request: ProfileUpdateRequest):

    profile.update_profile(
        username=request.username,
        difficulty=request.difficulty,
        learning_style=request.learning_style,
        weak_topics=request.weak_topics,
        strong_topics=request.strong_topics
    )

    return profile.get_profile(request.username)