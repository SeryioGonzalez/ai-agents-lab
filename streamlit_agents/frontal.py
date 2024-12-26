import os
import streamlit as st

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv(override=True)
az_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_URL")
az_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
az_openai_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Initialize the Azure OpenAI client
az_openai_client = AzureOpenAI(
    azure_endpoint=az_openai_endpoint,
    api_key=az_openai_api_key,
    api_version="2024-05-01-preview",
)

st.title("Basic Frontend")

SYSTEM_PROMPT = """
Limita tus respuestas a geografia.
Rechaza cortesmente responder a preguntas no relacionadas con la geografia
Usa lenguage coloquial y amigable.
Se breve en tus respuestas. Idealmente 1 o dos frases.
"""

# Initialize the session state and message container
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMPT})
                                                                                   #st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMT})
    
# Print all messages in session state
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Wait for user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Print user input
    with st.chat_message("user"):
        st.markdown(prompt)
    # Get response from LLM
    with st.chat_message("assistant"):
        stream = az_openai_client.chat.completions.create(
            model=az_openai_deployment_name,
            messages=st.session_state.messages,
            stream=True,
        )
        # Print response from LLM
        response = st.write_stream(stream)
    # Store response in session state
    st.session_state.messages.append({"role": "assistant", "content": response})