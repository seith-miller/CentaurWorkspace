import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from centaur_workspace.llm_providers.anthropic_provider import AnthropicProvider
from centaur_workspace.llm_providers.base import ChatMessage


@pytest.fixture
def mock_anthropic():
    with patch(
        "centaur_workspace.llm_providers.anthropic_provider.Anthropic"
    ) as mock_sync, patch(
        "centaur_workspace.llm_providers.anthropic_provider.AsyncAnthropic"
    ) as mock_async:
        mock_sync_instance = MagicMock()
        mock_async_instance = AsyncMock()
        mock_sync.return_value = mock_sync_instance
        mock_async.return_value = mock_async_instance
        yield mock_sync_instance, mock_async_instance


@pytest.mark.unit
class TestAnthropicProvider:
    def test_anthropic_provider_initialization(self):
        with patch(
            "centaur_workspace.llm_providers.anthropic_provider.Anthropic"
        ) as MockAnthropic, patch(
            "centaur_workspace.llm_providers.anthropic_provider.AsyncAnthropic"
        ) as MockAsyncAnthropic:
            provider = AnthropicProvider(api_key="test_key")
            assert provider.api_key == "test_key"
            assert provider.model == "claude-3-sonnet-20240229"
            MockAnthropic.assert_called_once_with(api_key="test_key")
            MockAsyncAnthropic.assert_called_once_with(api_key="test_key")

    def test_generate_text(self, mock_anthropic):
        mock_sync, _ = mock_anthropic
        mock_sync.messages.create.return_value.content = [
            MagicMock(text="Generated text")
        ]

        provider = AnthropicProvider(api_key="test_key")
        result = provider.generate_text("Test prompt")

        assert result == "Generated text"
        mock_sync.messages.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_text_async(self, mock_anthropic):
        _, mock_async = mock_anthropic
        mock_async.messages.create.return_value = AsyncMock()
        mock_async.messages.create.return_value.content = [
            AsyncMock(text="Async generated text")
        ]

        provider = AnthropicProvider(api_key="test_key")
        result = await provider.generate_text_async("Test prompt")

        assert result == "Async generated text"
        mock_async.messages.create.assert_called_once()

    def test_generate_chat_completion(self, mock_anthropic):
        mock_sync, _ = mock_anthropic
        mock_sync.messages.create.return_value.content = [
            MagicMock(text="Chat completion")
        ]

        provider = AnthropicProvider(api_key="test_key")
        messages = [ChatMessage(role="user", content="Hello")]
        result = provider.generate_chat_completion(messages)

        assert result == "Chat completion"
        mock_sync.messages.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_chat_completion_async(self, mock_anthropic):
        _, mock_async = mock_anthropic
        mock_async.messages.create.return_value = AsyncMock()
        mock_async.messages.create.return_value.content = [
            AsyncMock(text="Async chat completion")
        ]

        provider = AnthropicProvider(api_key="test_key")
        messages = [ChatMessage(role="user", content="Hello")]
        result = await provider.generate_chat_completion_async(messages)

        assert result == "Async chat completion"
        mock_async.messages.create.assert_called_once()
