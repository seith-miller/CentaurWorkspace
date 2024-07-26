import pytest
from centaur_workspace.llm_providers.base import BaseLLMProvider, ChatMessage
from centaur_workspace.llm_providers.openai_provider import OpenAIProvider


@pytest.fixture
def openai_provider():
    return OpenAIProvider()


def test_openai_provider_initialization(openai_provider):
    assert isinstance(openai_provider, BaseLLMProvider)
    assert isinstance(openai_provider, OpenAIProvider)


@pytest.mark.asyncio
async def test_openai_provider_generate_text(openai_provider):
    prompt = "Hello, world!"
    response = openai_provider.generate_text(prompt)
    assert isinstance(response, str)
    assert len(response) > 0

    async_response = await openai_provider.generate_text_async(prompt)
    assert isinstance(async_response, str)
    assert len(async_response) > 0


@pytest.mark.asyncio
async def test_openai_provider_generate_chat_completion(openai_provider):
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(role="user", content="What's the capital of France?"),
    ]
    response = openai_provider.generate_chat_completion(messages)
    assert isinstance(response, str)
    assert "Paris" in response

    async_response = await openai_provider.generate_chat_completion_async(messages)
    assert isinstance(async_response, str)
    assert "Paris" in async_response
