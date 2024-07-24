import pytest
from unittest.mock import patch, MagicMock
from centaur_workspace.tools.code_writing_tool import CodeWritingTool


@pytest.fixture
def mock_openai():
    with patch("centaur_workspace.tools.code_writing_tool.OpenAI") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance


def test_code_writing_tool_initialization(mock_openai):
    tool = CodeWritingTool()
    assert tool.name == "Code Writing Tool"
    assert "generates Python code" in tool.description


def test_code_writing_tool_run(mock_openai):
    tool = CodeWritingTool()
    mock_openai.chat.completions.create.return_value.choices[
        0
    ].message.content = "def example_function():\n    pass"
    result = tool._run("create an example function")
    assert "```python" in result
    assert "def example_function():" in result
    assert "```" in result


def test_code_writing_tool_run_empty_task():
    tool = CodeWritingTool()
    with pytest.raises(ValueError, match="Task cannot be empty."):
        tool._run("")


def test_code_writing_tool_run_no_response(mock_openai):
    tool = CodeWritingTool()
    mock_openai.chat.completions.create.return_value.choices = []
    result = tool._run("create an example function")
    assert "An error occurred" in result
    assert "No response generated" in result


def test_code_writing_tool_run_empty_response(mock_openai):
    tool = CodeWritingTool()
    mock_openai.chat.completions.create.return_value.choices[0].message.content = ""
    result = tool._run("create an example function")
    assert "An error occurred" in result
    assert "Generated code is empty" in result


@pytest.mark.asyncio
async def test_code_writing_tool_arun(mock_openai):
    tool = CodeWritingTool()
    mock_openai.chat.completions.create.return_value.choices[
        0
    ].message.content = "async def async_function():\n    pass"
    result = await tool._arun("create an async function")
    assert "```python" in result
    assert "async def async_function():" in result
    assert "```" in result
