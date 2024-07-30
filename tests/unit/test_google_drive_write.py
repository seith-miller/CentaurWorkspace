import pytest
from unittest.mock import MagicMock, patch
from centaur_workspace.tools.google_drive.write import GoogleDriveWriteTool


@pytest.fixture
def mock_service():
    mock = MagicMock()
    mock.files().get().execute.return_value = {"mimeType": "text/plain"}
    return mock


@pytest.fixture
def write_tool(mock_service):
    with patch(
        (
            "centaur_workspace.tools.google_drive.write."
            "GoogleDriveBaseTool._get_drive_service"
        ),
        return_value=mock_service,
    ):
        return GoogleDriveWriteTool()


def test_write_regular_file(write_tool):
    result = write_tool._run("file_id", "New content")
    assert "Content written to file with ID: file_id" in result


def test_write_google_doc(write_tool, mock_service):
    mock_service.files().get().execute.return_value = {
        "mimeType": "application/vnd.google-apps.document"
    }
    result = write_tool._run("doc_id", "New content")
    assert "Content written to Google Doc with ID: doc_id" in result
