from fastapi import APIRouter

from app.services.profile.profile_service import ProfileService

router = APIRouter()

profile = ProfileService()


@router.get("/profile/{username}")

async def get_profile(

    username: str

):

    return profile.get_profile(

        username

    )