import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from centaur_workspace.tools.code_writing_tool import CodeWritingTool


@pytest.fixture
def mock_openai():
    with patch("centaur_workspace.tools.code_writing_tool.OpenAI") as mock_sync, patch(
        "centaur_workspace.tools.code_writing_tool.AsyncOpenAI"
    ) as mock_async:
        mock_sync_instance = MagicMock()
        mock_async_instance = AsyncMock()
        mock_sync.return_value = mock_sync_instance
        mock_async.return_value = mock_async_instance
        yield mock_sync_instance, mock_async_instance


def test_code_writing_tool_initialization(mock_openai):
    tool = CodeWritingTool()
    assert tool.name == "Code Writing Tool"
    assert "generates Python code" in tool.description


def test_code_writing_tool_run(mock_openai):
    mock_sync, _ = mock_openai
    tool = CodeWritingTool()
    mock_sync.chat.completions.create.return_value.choices[
        0
    ].message.content = "def example_function():\n    pass"
    result = tool._run("create an example function")
    assert "def example_function():" in result
    assert "pass" in result


@pytest.mark.asyncio
async def test_code_writing_tool_arun(mock_openai):
    _, mock_async = mock_openai
    tool = CodeWritingTool()
    mock_async.chat.completions.create.return_value.choices[
        0
    ].message.content = "async def async_function():\n    pass"
    result = await tool._arun("create an async function")
    assert "async def async_function():" in result
    assert "pass" in result


def test_code_writing_tool_run_empty_task(mock_openai):
    tool = CodeWritingTool()
    with pytest.raises(ValueError, match="Task cannot be empty."):
        tool._run("")


@pytest.mark.asyncio
async def test_code_writing_tool_arun_empty_task(mock_openai):
    tool = CodeWritingTool()
    with pytest.raises(ValueError, match="Task cannot be empty."):
        await tool._arun("")


def test_code_writing_tool_run_no_response(mock_openai):
    mock_sync, _ = mock_openai
    tool = CodeWritingTool()
    mock_sync.chat.completions.create.return_value.choices = []
    result = tool._run("create an example function")
    assert "An error occurred" in result
    assert "No response generated" in result


@pytest.mark.asyncio
async def test_code_writing_tool_arun_no_response(mock_openai):
    _, mock_async = mock_openai
    tool = CodeWritingTool()
    mock_async.chat.completions.create.return_value.choices = []
    result = await tool._arun("create an example function")
    assert "An error occurred" in result
    assert "No response generated" in result
