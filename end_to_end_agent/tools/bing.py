# tools/bing.py
import logging
import requests
from config.env_loader import BING_API_KEY

logger = logging.getLogger(__name__)

def search_for_data_in_bing(query: str) -> str:
    """
    Search the Bing Web Search API and return the first result snippet.
    """ 
    logger.info(f"Searching Bing for query: {query}")

    headers = {
        "Ocp-Apim-Subscription-Key": BING_API_KEY
    }
    params = {
        "q": query,
        "count": 1  # Only request 1 result
    }

    response = requests.get(
        "https://api.bing.microsoft.com/v7.0/search",
        headers=headers,
        params=params
    )
    response.raise_for_status()
    data = response.json()

    if "webPages" in data and "value" in data["webPages"] and len(data["webPages"]["value"]) > 0:
        first_result = data["webPages"]["value"][0]
        snippet = first_result.get("snippet", "No Snippet")
        return snippet
    else:
        return "No results found."
