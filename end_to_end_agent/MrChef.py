# MrChef.py
import logging
import streamlit as st
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.tools import FunctionTool

# Importamos el constructor del agente
from agent.tool_chat_agent import ToolChatAgent
# Importamos config
from config.env_loader import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT_NAME,
    AZURE_OPENAI_API_KEY
)
from config.telemetry import init_telemetry
# Importamos funciones/herramientas
from tools.bing import search_for_data_in_bing
from tools.azure_search import cusine_recipes_vector_search

# Configuramos un mensaje del sistema
SYSTEM_MESSAGE = """
Eres un experto en recetas de cocina, conceptos culinarios y busqueda de restaurantes.
Limita tus preguntas a recetas de cocina, conceptos culinarios y busqueda de restaurantes.
Se breve y conciso, usando un lenguaje coloquial.
Responde en el idioma de la pregunta
"""

PAGE_TITLE = "Agente Chef"
TEXT_INPUT_BANNER = "¿Sobre qué quieres preguntar?"

########################################################################################

if "has_run" not in st.session_state:
    init_telemetry()
    logger = logging.getLogger('streamlit_app')
    
    logger.info("Creating a new agent")
    # Creamos las herramientas
    llm = AzureOpenAI(
        engine=AZURE_OPENAI_DEPLOYMENT_NAME,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version="2024-05-01-preview"
    )

    # Creamos las herramientas
    search_bing_tool = FunctionTool.from_defaults(fn=search_for_data_in_bing)
    local_kb_tool   = FunctionTool.from_defaults(fn=cusine_recipes_vector_search)

    # Creamos el agente y lo guardamos en session
    st.session_state.agent = ToolChatAgent(
        llm=llm,
        system_message=SYSTEM_MESSAGE,
        tools=[search_bing_tool, local_kb_tool]
    )

    st.session_state.has_run = True

st.title(PAGE_TITLE)

for message in st.session_state.agent.get_chat_history():
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Wait for user input
if user_prompt := st.chat_input(TEXT_INPUT_BANNER):
    # Print user input
    with st.chat_message("user"):
        st.markdown(user_prompt)
    # Get response from LLM
    with st.chat_message("assistant"):
        response = st.session_state.agent.chat(user_prompt)
        # Print response from LLM
        st.markdown(response)
