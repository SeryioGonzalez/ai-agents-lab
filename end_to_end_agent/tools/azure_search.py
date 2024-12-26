# tools/azure_search.py

import logging

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from config.env_loader import (
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_INDEX_NAME,
    AZURE_SEARCH_API_KEY,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME,
    AZURE_OPENAI_ENDPOINT
)

# Instanciamos la clase de embeddings de AzureOpenAI
# (Podrías mover este bloque si preferís centralizar la configuración de LLM)
azure_openai_embeddings = AzureOpenAIEmbedding(
    deployment_name=AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-05-01-preview"
)

search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
)

logger = logging.getLogger(__name__)

MAX_DOCS = 3
VECTOR_FIELDS = ["nombre_vector", "pasos_vector"]
SELECT_FIELDS = ["nombre, pasos, valor_nutricional"]

def cusine_recipes_vector_search(recipe_query: str):
    """Search for cuisine recipes in the Azure Search knowledge base."""

    logger.info(f"Calling the local kb with query: {recipe_query}")

    query_embeddings = azure_openai_embeddings.get_text_embedding(recipe_query)

    vector_query = VectorizedQuery(
        vector=query_embeddings,
        k_nearest_neighbors=MAX_DOCS,
        fields=",".join(VECTOR_FIELDS)
    )

    results = search_client.search(  
        search_text=None,  
        vector_queries=[vector_query],
        select=SELECT_FIELDS,
        top=MAX_DOCS
    ) 

    logger.info(f"Search results: {results.get_count()}")

    return results
