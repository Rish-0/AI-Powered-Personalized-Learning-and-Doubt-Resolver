from app.services.memory.memory_service import MemoryService


class ConversationService:

    def __init__(self):

        self.memory = MemoryService()

    def get_recent_context(self):

        rows = self.memory.history()

        context = ""

        for row in rows:

            context += f"""

User

{row['question']}

Assistant

{row['answer']}

"""

        return context