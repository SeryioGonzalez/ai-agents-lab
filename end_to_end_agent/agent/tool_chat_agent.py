# agent/tool_chat_agent.py
import json
import logging

from typing import Sequence
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool
from llama_index.llms.azure_openai import AzureOpenAI
from openai.types.chat import ChatCompletionMessageToolCall

class ToolChatAgent:
    def __init__(
        self,
        llm: AzureOpenAI,
        system_message: str,
        tools: Sequence[BaseTool] = []
    ) -> None:
        self._llm = llm
        self._tools = {tool.metadata.name: tool for tool in tools}
        self._chat_history = [ChatMessage(role="system", content=system_message)]

    def get_chat_history(self):

        basic_chat_history = [ {"role": message.role.value, "content": message.content} for message in self._chat_history]    

        return basic_chat_history

    def chat(self, message: str) -> str:
        chat_history = self._chat_history
        chat_history.append(ChatMessage(role="user", content=message))

        # Convert LlamaIndex Tools to OpenAI Tools
        tools = [tool.metadata.to_openai_tool() for tool in self._tools.values()]

        # Get the AI response
        ai_message = self._llm.chat(chat_history, tools=tools).message
        additional_kwargs = ai_message.additional_kwargs
        chat_history.append(ai_message)

        # Handle tool calls if present
        tool_calls = additional_kwargs.get("tool_calls", None)
        if tool_calls:
            for tool_call in tool_calls:
                function_message = self._call_function(tool_call)
                chat_history.append(function_message)

                ai_message = self._llm.chat(chat_history).message
                chat_history.append(ai_message)

        return ai_message.content

    def _call_function(self, tool_call: ChatCompletionMessageToolCall) -> ChatMessage:
        id_ = tool_call.id
        function_call = tool_call.function
        tool = self._tools[function_call.name]
        output = tool(**json.loads(function_call.arguments))

        return ChatMessage(
            name=function_call.name,
            content=str(output),
            role="tool",
            additional_kwargs={
                "tool_call_id": id_,
                "name": function_call.name,
            },
        )