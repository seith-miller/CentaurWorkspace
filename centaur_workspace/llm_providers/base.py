from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        pass

    @abstractmethod
    async def generate_text_async(self, prompt: str, max_tokens: int = 500) -> str:
        pass

    @abstractmethod
    def generate_chat_completion(
        self, messages: List[ChatMessage], max_tokens: int = 500
    ) -> str:
        pass

    @abstractmethod
    async def generate_chat_completion_async(
        self, messages: List[ChatMessage], max_tokens: int = 500
    ) -> str:
        pass
