# centaur_workspace/tools/timestamp_tool.py
from datetime import datetime
from crewai_tools import BaseTool


class TimestampTool(BaseTool):
    name: str = "Timestamp Tool"
    description: str = (
        "Provides the current timestamp in the format yyyy-mm-dd hh:mm:ss."
    )

    def _run(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def _arun(self) -> str:
        return self._run()
