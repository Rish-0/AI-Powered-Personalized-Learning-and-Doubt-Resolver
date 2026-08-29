from tavily import TavilyClient

from app.core.config import settings


class TavilyService:

    def __init__(self):

        self.client = TavilyClient(

            api_key=settings.TAVILY_API_KEY

        )

    def search(self, query: str):

        response = self.client.search(

            query=query,

            search_depth="advanced",

            max_results=5

        )

        return response["results"]