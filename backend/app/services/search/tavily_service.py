import logging
from tavily import TavilyClient
from app.core.config import settings

logger = logging.getLogger(__name__)


class TavilyService:

    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.client = None
        if self.api_key:
            try:
                self.client = TavilyClient(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize TavilyClient: {e}")

    def search(self, query: str):
        if not self.client:
            logger.warning("TavilyClient not configured or missing API key.")
            return []

        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=5
            )
            return response.get("results", [])
        except Exception as e:
            logger.error(f"Tavily search error for '{query}': {e}")
            return []
