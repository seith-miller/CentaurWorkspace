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
        print("Files listed by GoogleDriveListTool:\n", result)
        assert isinstance(result, str)
        if "An error occurred: Invalid or missing credentials" in result:
            pytest.skip("Authentication failed. Please run the authentication script.")
        else:
            assert "No files found" in result or "(" in result

    def test_integration_read_file(self, tools):
        # Specific file ID for the Google Doc "start here"
        file_id = "1lNA7mB8MOj8Jy-TVSikTUg5onUemFFyqgI_aM7OXtbc"

        initial_content = tools["read"]._run(file_id)
        print("Initial content read from Google Doc:\n", initial_content)
        assert isinstance(initial_content, str)
        assert initial_content.strip() == "abc123"
