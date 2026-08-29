from groq import Groq
from app.core.config import settings


class GroqService:

    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def generate_response(self, prompt: str):
        try:
            completion = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=1024
            )

            return completion.choices[0].message.content
        except Exception as e:
            print("Groq Error:", e)
            raise