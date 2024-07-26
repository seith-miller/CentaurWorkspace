import pytest
from unittest.mock import MagicMock, AsyncMock
from centaur_workspace.tools.code_writing_tool import CodeWritingTool
from centaur_workspace.llm_providers.base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        return "def example_function():\n    pass"

    async def generate_text_async(self, prompt: str, max_tokens: int = 500) -> str:
        return "async def async_function():\n    pass"

    def generate_chat_completion(self, messages: list, max_tokens: int = 500) -> str:
        return "def example_function():\n    pass"

    async def generate_chat_completion_async(
        self, messages: list, max_tokens: int = 500
    ) -> str:
        return "async def async_function():\n    pass"


@pytest.mark.unit
class TestCodeWritingTool:
    @pytest.fixture
    def mock_llm_provider(self):
        return MockLLMProvider()

    def test_code_writing_tool_initialization(self, mock_llm_provider):
        tool = CodeWritingTool(llm_provider=mock_llm_provider)
        assert tool.name == "Code Writing Tool"
        assert "generates Python code" in tool.description

    def test_code_writing_tool_run(self, mock_llm_provider):
        tool = CodeWritingTool(llm_provider=mock_llm_provider)
        result = tool._run("create an example function")
        assert "def example_function():" in result
        assert "pass" in result

    @pytest.mark.asyncio
    async def test_code_writing_tool_arun(self, mock_llm_provider):
        tool = CodeWritingTool(llm_provider=mock_llm_provider)
        result = await tool._arun("create an async function")
        assert "async def async_function():" in result
        assert "pass" in result

    def test_code_writing_tool_run_empty_task(self, mock_llm_provider):
        tool = CodeWritingTool(llm_provider=mock_llm_provider)
        with pytest.raises(ValueError, match="Task cannot be empty."):
            tool._run("")

    @pytest.mark.asyncio
    async def test_code_writing_tool_arun_empty_task(self, mock_llm_provider):
        tool = CodeWritingTool(llm_provider=mock_llm_provider)
        with pytest.raises(ValueError, match="Task cannot be empty."):
            await tool._arun("")

    def test_code_writing_tool_run_no_response(self, mock_llm_provider):
        mock_llm_provider.generate_chat_completion = MagicMock(return_value="")
        tool = CodeWritingTool(llm_provider=mock_llm_provider)
        result = tool._run("create an example function")
        assert "An error occurred" in result
        assert "Generated code is empty" in result

    @pytest.mark.asyncio
    async def test_code_writing_tool_arun_no_response(self, mock_llm_provider):
        mock_llm_provider.generate_chat_completion_async = AsyncMock(return_value="")
        tool = CodeWritingTool(llm_provider=mock_llm_provider)
        result = await tool._arun("create an example function")
        assert "An error occurred" in result
        assert "Generated code is empty" in result
