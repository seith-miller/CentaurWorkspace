import pytest
import uuid
from unittest.mock import patch
from centaur_workspace.tools.google_drive.create import GoogleDriveCreateTool
from centaur_workspace.tools.google_drive.navigate import GoogleDriveNavigationTool


@pytest.mark.integration
class TestGoogleDriveCreateIntegration:
    @pytest.fixture(scope="class")
    def create_tool(self):
        with patch(
            "centaur_workspace.tools.google_drive.create."
            "GoogleDriveBaseTool._get_drive_service"
        ) as mock_service:
            mock_service.return_value.files().create().execute.return_value = {
                "id": "new_folder_id"
            }
            yield GoogleDriveCreateTool()

    @pytest.fixture(scope="class")
    def navigation_tool(self):
        with patch(
            "centaur_workspace.tools.google_drive.navigate."
            "GoogleDriveBaseTool._get_drive_service"
        ) as mock_service:
            mock_service.return_value.files().list().execute.return_value = {
                "files": [
                    {
                        "id": "new_folder_id",
                        "name": "Test Folder",
                        "mimeType": "application/vnd.google-apps.folder",
                    }
                ]
            }
            yield GoogleDriveNavigationTool()

    def test_create_folder(self, create_tool, navigation_tool):
        folder_name = "Test Folder"
        result = create_tool._run(folder_name, "application/vnd.google-apps.folder")
        assert "Folder created with ID: new_folder_id" in result

        root_contents = navigation_tool._run()
        assert "Test Folder" in root_contents

    def test_create_file(self, create_tool, navigation_tool):
        with patch(
            "centaur_workspace.tools.google_drive.create."
            "GoogleDriveBaseTool._get_drive_service"
        ) as mock_service:
            mock_service.return_value.files().create().execute.return_value = {
                "id": "new_file_id"
            }
            create_tool = GoogleDriveCreateTool()

        file_name = f"Test File {uuid.uuid4()}.txt"
        content = "This is a test file created by integration test."
        result = create_tool._run(file_name, "text/plain", content=content)
        assert "File created with ID: new_file_id" in result

        with patch(
            "centaur_workspace.tools.google_drive.navigate."
            "GoogleDriveBaseTool._get_drive_service"
        ) as mock_service:
            mock_service.return_value.files().list().execute.return_value = {
                "files": [
                    {"id": "new_file_id", "name": file_name, "mimeType": "text/plain"}
                ]
            }
            navigation_tool = GoogleDriveNavigationTool()

        root_contents = navigation_tool._run()
        assert file_name in root_contents
