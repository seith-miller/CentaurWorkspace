import pytest
from centaur_workspace.tools.google_drive.read import GoogleDriveReadTool


@pytest.mark.integration
class TestGoogleDriveReadIntegration:
    @pytest.fixture(scope="class")
    def read_tool(self):
        return GoogleDriveReadTool()

    def test_read_file(self, read_tool):
        # Assuming there's a known file in the root directory for testing
        file_name = (
            "test_file.txt"  # Replace with a known file name in your root directory
        )
        content = read_tool._run(file_name)
        assert isinstance(content, str)
        assert len(content) > 0  # Ensure some content was read
