from crewai_tools import BaseTool
from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv
from pydantic import PrivateAttr
from openai.types.chat import ChatCompletionMessageParam


class CodeWritingTool(BaseTool):
    name: str = "Code Writing Tool"
    description: str = "A tool that generates Python code using an LLM."
    _sync_client: OpenAI = PrivateAttr()
    _async_client: AsyncOpenAI = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self._sync_client = OpenAI(api_key=api_key)
        self._async_client = AsyncOpenAI(api_key=api_key)

    def _generate_messages(self, task: str) -> list[ChatCompletionMessageParam]:
        return [
            {
                "role": "system",
                "content": (
                    "You are a skilled Python programmer. Generate concise, "
                    "working Python code based on the given task. Do not include "
                    "any markdown formatting or code block indicators."
                ),
            },
            {
                "role": "user",
                "content": f"Write Python code to {task}. Provide only the code "
                "without any explanations or markup.",
            },
        ]

    def _run(self, task: str) -> str:
        if not task:
            raise ValueError("Task cannot be empty.")

        try:
            response = self._sync_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self._generate_messages(task),
                max_tokens=500,
                n=1,
                temperature=0.7,
            )

            if not response.choices:
                raise ValueError("No response generated from the language model.")

            code = response.choices[0].message.content.strip()
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
            response = await self._async_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self._generate_messages(task),
                max_tokens=500,
                n=1,
                temperature=0.7,
            )

            if not response.choices:
                raise ValueError("No response generated from the language model.")

            code = response.choices[0].message.content.strip()
            if not code:
                raise ValueError("Generated code is empty.")

            return code

        except Exception as e:
            error_message = f"An error occurred while generating code: {str(e)}"
            print(f"Error in CodeWritingTool: {error_message}")
            return error_message
