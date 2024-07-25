import pytest
from centaur_workspace.tools.google_drive_tool import (
    GoogleDriveListTool,
    GoogleDriveReadTool,
    GoogleDriveWriteTool,
)


@pytest.mark.integration
class TestGoogleDriveIntegrationTools:
    @pytest.fixture(scope="class")
    def tools(self):
        return {
            "list": GoogleDriveListTool(),
            "read": GoogleDriveReadTool(),
            "write": GoogleDriveWriteTool(),
        }

    def test_integration_list_files(self, tools):
        result = tools["list"]._run()
        print(
            "Files listed by GoogleDriveListTool:\n", result
        )  # Print the listed files
        assert isinstance(result, str)
        if "An error occurred: Invalid or missing credentials" in result:
            pytest.skip("Authentication failed. Please run the authentication script.")
        else:
            assert "No files found" in result or "(" in result

    def test_integration_read_file(self, tools):
        files_list = tools["list"]._run()
        print(
            "Files listed by GoogleDriveListTool for reading:\n", files_list
        )  # Print the listed files
        file_id = next(
            (
                line.split("(")[1].split(")")[0]
                for line in files_list.split("\n")
                if "application/vnd.google-apps.document" in line
            ),
            None,
        )
        if not file_id:
            pytest.skip("No Google Doc found to test read/write operations")

        initial_content = tools["read"]._run(file_id)
        print(
            "Initial content read from Google Doc:\n", initial_content
        )  # Print the content
        assert isinstance(initial_content, str)
