import os
from typing import List
from anthropic import Anthropic, AsyncAnthropic
from .base import BaseLLMProvider, ChatMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AnthropicProvider(BaseLLMProvider):
    def __init__(self, api_key: str = None, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is not set")
        self.model = model
        self.client = Anthropic(api_key=self.api_key)
        self.async_client = AsyncAnthropic(api_key=self.api_key)

    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            return f"An error occurred while generating text: {str(e)}"

    async def generate_text_async(self, prompt: str, max_tokens: int = 500) -> str:
        try:
            response = await self.async_client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            return f"An error occurred while generating text asynchronously: {str(e)}"

    def generate_chat_completion(
        self, messages: List[ChatMessage], max_tokens: int = 500
    ) -> str:
        try:
            anthropic_messages = [
                {"role": msg.role, "content": msg.content} for msg in messages
            ]
            response = self.client.messages.create(
                model=self.model, max_tokens=max_tokens, messages=anthropic_messages
            )
            return response.content[0].text
        except Exception as e:
            return f"An error occurred while generating chat completion: {str(e)}"

    async def generate_chat_completion_async(
        self, messages: List[ChatMessage], max_tokens: int = 500
    ) -> str:
        try:
            anthropic_messages = [
                {"role": msg.role, "content": msg.content} for msg in messages
            ]
            response = await self.async_client.messages.create(
                model=self.model, max_tokens=max_tokens, messages=anthropic_messages
            )
            return response.content[0].text
        except Exception as e:
            return (
                "An error occurred while generating chat completion "
                f"asynchronously: {str(e)}"
            )
