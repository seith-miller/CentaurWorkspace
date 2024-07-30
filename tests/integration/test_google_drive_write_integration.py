import pytest
from unittest.mock import patch
from centaur_workspace.tools.google_drive.write import GoogleDriveWriteTool
from centaur_workspace.tools.google_drive.read import GoogleDriveReadTool
from centaur_workspace.tools.google_drive.navigate import GoogleDriveNavigationTool


@pytest.mark.integration
class TestGoogleDriveWriteIntegration:
    @pytest.fixture(scope="class")
    def mock_service(self):
        with patch(
            (
                "centaur_workspace.tools.google_drive.base."
                "GoogleDriveBaseTool._get_drive_service"
            )
        ) as mock:
            yield mock

    @pytest.fixture(scope="class")
    def write_tool(self, mock_service):
        return GoogleDriveWriteTool(service=mock_service.return_value)

    @pytest.fixture(scope="class")
    def read_tool(self, mock_service):
        return GoogleDriveReadTool(service=mock_service.return_value)

    @pytest.fixture(scope="class")
    def navigation_tool(self, mock_service):
        return GoogleDriveNavigationTool(service=mock_service.return_value)

    def test_write_and_read_file(
        self, write_tool, read_tool, navigation_tool, mock_service
    ):
        # Mock navigation
        mock_service.return_value.files().list().execute.return_value = {
            "files": [
                {
                    "id": "file_id",
                    "name": "Test File (file_id)",
                    "mimeType": "text/plain",
                }
            ]
        }
        root_contents = navigation_tool._run()

        file_id = None
        for line in root_contents.split("\n"):
            if "Test File" in line:
                parts = line.split("(")
                if len(parts) > 1:
                    file_id = parts[1].split(")")[0]
                    break

        assert file_id, "No file found in root directory"

        # Mock write operation
        mock_service.return_value.files().get().execute.return_value = {
            "mimeType": "text/plain"
        }
        mock_service.return_value.files().update().execute.return_value = {
            "id": file_id
        }

        new_content = "This is a test content written by integration test."
        write_result = write_tool._run(file_id, new_content)
        assert f"Content written to file with ID: {file_id}" in write_result

        # Mock read operation
        mock_service.return_value.files().get().execute.return_value = {
            "mimeType": "text/plain"
        }
        mock_service.return_value.files().get_media().execute.return_value = (
            new_content.encode()
        )

        read_content = read_tool._run(file_id)
        assert new_content in read_content
