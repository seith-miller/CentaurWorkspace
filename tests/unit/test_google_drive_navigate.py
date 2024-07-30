import pytest
from unittest.mock import MagicMock, patch
from centaur_workspace.tools.google_drive.navigate import GoogleDriveNavigationTool


@pytest.fixture
def mock_service():
    mock = MagicMock()
    mock.files().list().execute.return_value = {
        "files": [
            {"id": "1", "name": "File1", "mimeType": "text/plain"},
            {
                "id": "2",
                "name": "Folder1",
                "mimeType": "application/vnd.google-apps.folder",
            },
        ]
    }
    return mock


@pytest.fixture
def navigation_tool(mock_service):
    with patch(
        (
            "centaur_workspace.tools.google_drive.navigate."
            "GoogleDriveBaseTool._get_drive_service"
        ),
        return_value=mock_service,
    ):
        return GoogleDriveNavigationTool()


def test_list_folder_contents(navigation_tool):
    result = navigation_tool._run()
    assert "File1" in result
    assert "Folder1" in result
