import pytest
from centaur_workspace.tools.google_drive_tool import (
    GoogleDriveListTool,
    GoogleDriveReadTool,
    GoogleDriveWriteTool,
)
from centaur_workspace.tools.timestamp_tool import TimestampTool


@pytest.mark.manual
@pytest.mark.integration
class TestGoogleDriveManualTools:
    @pytest.fixture(scope="class")
    def tools(self):
        return {
            "list": GoogleDriveListTool(),
            "read": GoogleDriveReadTool(),
            "write": GoogleDriveWriteTool(),
            "timestamp": TimestampTool(),
        }

    def test_manual_write_file(self, tools):
        # Specific file ID for the Google Doc "write_test"
        file_id = "1WmG6JevjyHseFPZLvzZnLwVY8mJVQAx2SRAHacsAdaQ"

        timestamp = tools["timestamp"]._run()
        new_content = f"Test content written by GoogleDriveWriteTool at {timestamp}"
        write_result = tools["write"]._run(file_id, new_content)
        print("Write result:\n", write_result)

        # Verify the written content
        updated_content = tools["read"]._run(file_id)
        print(f"Updated content in write_test:\n{updated_content}")

        assert "Content written to file" in write_result
        assert new_content in updated_content
