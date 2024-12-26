
import os  
from openai import AzureOpenAI  

from dotenv import load_dotenv

load_dotenv(override=True)

endpoint = os.getenv("ENDPOINT_URL")  
deployment = os.getenv("DEPLOYMENT_NAME")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")  

SYSTEM_MESSAGE = "Eres un asistente de investigacion. Responde en base a tu cuerpo de conocimiento."

# Initialize Azure OpenAI client with key-based authentication    
az_openai_client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",  
)


# Prepare the chat prompt
messages = []
# Append the system message
messages.append({
    "role": "system",
    "content": SYSTEM_MESSAGE
})
# Chat loop
def chat_loop():
    print("Chat CLI with OpenAI (type 'exit' to quit)")
    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Add user input to messages
        messages.append({"role": "user", "content": user_input})

        # Call OpenAI API
        try:
            completion = az_openai_client.chat.completions.create(
                model=deployment,
                messages=messages
            )

            # Get the assistant's message
            message = completion.choices[0].message
            messages.append({"role": "assistant", "content": message.content})

            # Print assistant's response
            print(f"Assistant: {message.content}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    chat_loop()