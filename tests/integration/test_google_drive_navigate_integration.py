import pytest
from centaur_workspace.tools.google_drive.navigate import GoogleDriveNavigationTool


@pytest.mark.integration
class TestGoogleDriveNavigationIntegration:
    @pytest.fixture(scope="class")
    def navigation_tool(self):
        return GoogleDriveNavigationTool()

    def test_list_root_folder(self, navigation_tool):
        result = navigation_tool._run()
        assert isinstance(result, str)
        assert "Files and folders in root directory:" in result

    def test_root_folder_content(self, navigation_tool):
        result = navigation_tool._run()
        assert (
            "📁" in result or "📄" in result
        )  # Ensure there's at least one file or folder
        assert "(ID:" in result  # Ensure IDs are present in the output
