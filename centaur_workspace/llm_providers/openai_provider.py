import os
from typing import List
from openai import OpenAI, AsyncOpenAI
from .base import BaseLLMProvider, ChatMessage


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is not set")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        self.async_client = AsyncOpenAI(api_key=self.api_key)

    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()

    async def generate_text_async(self, prompt: str, max_tokens: int = 500) -> str:
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()

    def generate_chat_completion(
        self, messages: List[ChatMessage], max_tokens: int = 500
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": msg.role, "content": msg.content} for msg in messages],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()

    async def generate_chat_completion_async(
        self, messages: List[ChatMessage], max_tokens: int = 500
    ) -> str:
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=[{"role": msg.role, "content": msg.content} for msg in messages],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
