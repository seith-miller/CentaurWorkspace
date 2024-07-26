from crewai_tools import BaseTool
from pydantic import PrivateAttr
from centaur_workspace.llm_providers.base import BaseLLMProvider, ChatMessage
from centaur_workspace.llm_providers.openai_provider import OpenAIProvider


class CodeWritingTool(BaseTool):
    name: str = "Code Writing Tool"
    description: str = "A tool that generates Python code using an LLM."
    _llm_provider: BaseLLMProvider = PrivateAttr()

    def __init__(self, llm_provider: BaseLLMProvider = None, **data):
        super().__init__(**data)
        self._llm_provider = llm_provider or OpenAIProvider()

    def _generate_messages(self, task: str) -> list[ChatMessage]:
        return [
            ChatMessage(
                role="system",
                content="You are a skilled Python programmer. "
                "Generate concise, "
                "working Python code based on the given task."
                "Do not include any markdown, "
                "formatting or code block indicators.",
            ),
            ChatMessage(
                role="user",
                content=(
                    f"Write Python code to {task}. "
                    "Provide only the code without any explanations or markup."
                ),
            ),
        ]

    def _run(self, task: str) -> str:
        if not task:
            raise ValueError("Task cannot be empty.")

        try:
            messages = self._generate_messages(task)
            code = self._llm_provider.generate_chat_completion(messages, max_tokens=500)
            if not code:
                raise ValueError("Generated code is empty.")
            return code
        except Exception as e:
            error_message = f"An error occurred while generating code: {str(e)}"
            print(f"Error in CodeWritingTool: {error_message}")
            return error_message

    async def _arun(self, task: str) -> str:
        if not task:
            raise ValueError("Task cannot be empty.")

        try:
            messages = self._generate_messages(task)
            code = await self._llm_provider.generate_chat_completion_async(
                messages, max_tokens=500
            )
            if not code:
                raise ValueError("Generated code is empty.")
            return code
        except Exception as e:
            error_message = f"An error occurred while generating code: {str(e)}"
            print(f"Error in CodeWritingTool: {error_message}")
            return error_message
