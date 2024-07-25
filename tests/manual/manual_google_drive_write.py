import pytest
from centaur_workspace.tools.google_drive_tool import (
    GoogleDriveListTool,
    GoogleDriveReadTool,
    GoogleDriveWriteTool,
)


@pytest.mark.manual
@pytest.mark.integration
class TestGoogleDriveManualTools:
    @pytest.fixture(scope="class")
    def tools(self):
        return {
            "list": GoogleDriveListTool(),
            "read": GoogleDriveReadTool(),
            "write": GoogleDriveWriteTool(),
        }

    def test_manual_write_file(self, tools):
        files_list = tools["list"]._run()
        print("Files listed by GoogleDriveListTool for writing:\n", files_list)
        file_info = next(
            (
                line
                for line in files_list.split("\n")
                if "application/vnd.google-apps.document" in line
            ),
            None,
        )
        if not file_info:
            pytest.skip("No Google Doc found to test read/write operations")

        file_id = file_info.split("(")[1].split(")")[0]
        file_name = file_info.split(" (")[0]

        print(f"Selected file for writing: {file_name} (ID: {file_id})")

        new_content = "Test content written by GoogleDriveWriteTool"
        write_result = tools["write"]._run(file_id, new_content)
        print("Write result:\n", write_result)

        # Verify the written content
        updated_content = tools["read"]._run(file_id)
        print(f"Updated content in {file_name}:\n", updated_content)

        assert "Content written to file" in write_result
        assert new_content in updated_content
