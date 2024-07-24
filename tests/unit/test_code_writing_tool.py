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
    assert "def example_function():" in result


@pytest.mark.asyncio
async def test_code_writing_tool_arun(mock_openai):
    tool = CodeWritingTool()
    mock_openai.chat.completions.create.return_value.choices[
        0
    ].message.content = "def async_function():\n    pass"
    result = await tool._arun("create an async function")
    assert "def async_function():" in result
