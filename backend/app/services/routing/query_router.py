class QueryRouter:

    @staticmethod
    def is_web_query(question: str):

        keywords = [

            "latest",

            "today",

            "current",

            "news",

            "recent",

            "2025",

            "2026",

            "internet"

        ]

        question = question.lower()

        return any(

            word in question

            for word in keywords

        )