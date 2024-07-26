# tests/unit/test_timestamp_tool.py
import pytest
from centaur_workspace.tools.timestamp_tool import TimestampTool


@pytest.mark.unit
class TestTimestampTool:
    def test_timestamp_tool_run(self):
        tool = TimestampTool()
        timestamp = tool._run()
        assert isinstance(timestamp, str)
        assert len(timestamp) == 19  # Length of the timestamp "yyyy-mm-dd hh:mm:ss"

    @pytest.mark.asyncio
    async def test_timestamp_tool_arun(self):
        tool = TimestampTool()
        timestamp = await tool._arun()
        assert isinstance(timestamp, str)
        assert len(timestamp) == 19
