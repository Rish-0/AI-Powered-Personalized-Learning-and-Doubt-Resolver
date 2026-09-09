from app.services.profile.profile_service import ProfileService


class PersonalizationService:

    def __init__(self):

        self.profile = ProfileService()

    def build_profile_context(

        self,

        username

    ):

        profile = self.profile.get_profile(

            username

        )

        return f"""

Difficulty

{profile["difficulty"]}

Learning Style

{profile["learning_style"]}

Weak Topics

{profile["weak_topics"]}

Strong Topics

{profile["strong_topics"]}

"""