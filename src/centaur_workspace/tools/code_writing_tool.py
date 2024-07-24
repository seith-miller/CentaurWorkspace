from crewai_tools import BaseTool
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import PrivateAttr


class CodeWritingTool(BaseTool):
    name: str = "Code Writing Tool"
    description: str = "A tool that generates Python code using an LLM."
    _client: OpenAI = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self._client = OpenAI(api_key=api_key)

    def _run(self, task: str) -> str:
        prompt = (
            f"Write Python code to {task}. "
            "Provide only the code without any explanations."
        )

        try:
            response = self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a skilled Python programmer. "
                        "Generate concise, working Python code "
                        "based on the given task.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                n=1,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"An error occurred while generating code: {str(e)}"

    async def _arun(self, task: str) -> str:
        # For simplicity, we're using the synchronous version here
        # In a real-world scenario, you'd want to use OpenAI's async API
        return self._run(task)
