import pytest
from unittest.mock import MagicMock, patch
from centaur_workspace.tools.google_drive.create import GoogleDriveCreateTool


@pytest.fixture
def mock_service():
    mock = MagicMock()
    mock.files().create().execute.return_value = {"id": "new_file_id"}
    return mock


@pytest.fixture
def create_tool(mock_service):
    with patch(
        (
            "centaur_workspace.tools.google_drive.create."
            "GoogleDriveBaseTool._get_drive_service"
        ),
        return_value=mock_service,
    ):
        return GoogleDriveCreateTool()


def test_create_folder(create_tool):
    result = create_tool._run("New Folder", "application/vnd.google-apps.folder")
    assert "Folder created with ID: new_file_id" in result


def test_create_file(create_tool):
    result = create_tool._run("New File", "text/plain", content="File content")
    assert "File created with ID: new_file_id" in result


def test_create_file_in_folder(create_tool):
    result = create_tool._run(
        "New File", "text/plain", parent_id="folder_id", content="File content"
    )
    assert "File created with ID: new_file_id" in result
