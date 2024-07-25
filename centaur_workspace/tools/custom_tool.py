from crewai_tools.tools import RagTool


class CustomTool(RagTool):
    name: str = "Custom Greeting Tool"
    description: str = "A tool that generates custom greetings."

    def _run(self, name: str = "User") -> str:
        return f"Hello, {name}! Welcome to our CrewAI project."
