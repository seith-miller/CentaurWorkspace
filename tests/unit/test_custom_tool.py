from dotenv import load_dotenv
from centaur_workspace.tools.custom_tool import CustomTool


def test_custom_tool():
    load_dotenv()  # This will load the API key from .env
    tool = CustomTool()
    result = tool._run("Alice")
    assert result == "Hello, Alice! Welcome to our CrewAI project."

    result = tool._run()
    assert result == "Hello, User! Welcome to our CrewAI project."
