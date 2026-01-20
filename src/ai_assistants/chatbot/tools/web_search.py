"""Web search tool using Tavily."""

from typing import Any, Dict, List, Optional

from ai_assistants.shared.config import settings
from ai_assistants.shared.logging import get_logger

logger = get_logger(__name__)


async def search_web(query: str, max_results: int = 5) -> Optional[Dict[str, Any]]:
    """Search the web using Tavily API.

    Args:
        query: The search query.
        max_results: Maximum number of results to return.

    Returns:
        Dictionary with 'content' and 'sources' keys, or None if search fails.
    """
    if not settings.tavily_api_key:
        logger.warning("Tavily API key not configured, skipping web search")
        return None

    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=settings.tavily_api_key)
        response = client.search(query, max_results=max_results)

        results: List[str] = []
        sources: List[str] = []

        for result in response.get("results", []):
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")

            results.append(f"**{title}**\n{content}")
            if url:
                sources.append(url)

        return {
            "content": "\n\n".join(results),
            "sources": sources,
        }

    except ImportError:
        logger.warning("tavily-python not installed, skipping web search")
        return None
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return None
