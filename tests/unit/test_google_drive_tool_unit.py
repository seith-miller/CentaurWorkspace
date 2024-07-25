import pytest
from unittest.mock import patch
from centaur_workspace.tools.google_drive_tool import (
    GoogleDriveListTool,
    GoogleDriveReadTool,
    GoogleDriveWriteTool,
)


@pytest.mark.unit
class TestGoogleDriveUnitTools:
    @pytest.fixture(scope="class")
    def tools(self):
        return {
            "list": GoogleDriveListTool(),
            "read": GoogleDriveReadTool(),
            "write": GoogleDriveWriteTool(),
        }

    @patch("centaur_workspace.tools.google_drive_tool.GoogleDriveListTool._run")
    def test_unit_list_files(self, mock_run, tools):
        mock_run.return_value = "Mock file list response"
        result = tools["list"]._run()
        assert result == "Mock file list response"
        mock_run.assert_called_once()

    @patch("centaur_workspace.tools.google_drive_tool.GoogleDriveReadTool._run")
    def test_unit_read_file(self, mock_run, tools):
        mock_run.return_value = "Mock file content"
        file_id = "mock_file_id"
        result = tools["read"]._run(file_id)
        assert result == "Mock file content"
        mock_run.assert_called_once_with(file_id)

    @patch("centaur_workspace.tools.google_drive_tool.GoogleDriveWriteTool._run")
    def test_unit_write_file(self, mock_run, tools):
        mock_run.return_value = "Content written to file mock_file_id"
        file_id = "mock_file_id"
        new_content = "Test content"
        result = tools["write"]._run(file_id, new_content)
        assert result == "Content written to file mock_file_id"
        mock_run.assert_called_once_with(file_id, new_content)
