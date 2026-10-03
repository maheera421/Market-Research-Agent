from tavily import TavilyClient

from app import config

_client = TavilyClient(api_key=config.TAVILY_API_KEY)


_CONTENT_CHAR_LIMIT = 500


def search(query: str, max_results: int = 3) -> list[dict]:
    response = _client.search(query, max_results=max_results)
    return [
        {
            "title": result["title"],
            "content": result["content"][:_CONTENT_CHAR_LIMIT],
            "url": result["url"],
        }
        for result in response["results"]
    ]
