import pytest
from centaur_workspace.llm_providers.anthropic_provider import AnthropicProvider
from centaur_workspace.llm_providers.base import ChatMessage


@pytest.mark.integration
class TestAnthropicProviderIntegration:
    @pytest.fixture(scope="class")
    def anthropic_provider(self):
        return AnthropicProvider()

    def test_generate_text(self, anthropic_provider):
        result = anthropic_provider.generate_text("Hello, world!")
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_generate_text_async(self, anthropic_provider):
        result = await anthropic_provider.generate_text_async("Hello, world!")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_generate_chat_completion(self, anthropic_provider):
        messages = [ChatMessage(role="user", content="What is the capital of France?")]
        result = anthropic_provider.generate_chat_completion(messages)
        assert isinstance(result, str)
        assert "Paris" in result

    @pytest.mark.asyncio
    async def test_generate_chat_completion_async(self, anthropic_provider):
        messages = [ChatMessage(role="user", content="What is the capital of France?")]
        result = await anthropic_provider.generate_chat_completion_async(messages)
        assert isinstance(result, str)
        assert "Paris" in result
