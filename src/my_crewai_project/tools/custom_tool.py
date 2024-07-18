from crewai_tools import BaseTool

class CustomTool(BaseTool):
    name: str = "Custom Greeting Tool"
    description: str = "A tool that generates custom greetings."

    def _run(self, name: str = "User") -> str:
        return f"Hello, {name}! Welcome to our CrewAI project."
