from pydantic import Field
from .base import GoogleDriveBaseTool, logger
import os


class GoogleDriveNavigationTool(GoogleDriveBaseTool):
    name: str = "Google Drive Navigation Tool"
    description: str = "List contents of Google Drive root folder"
    root_folder_id: str = Field(
        default_factory=lambda: os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID")
    )

    def _run(self):
        try:
            return self._list_root_folder()
        except Exception as e:
            logger.exception(
                f"An error occurred in GoogleDriveNavigationTool: {str(e)}"
            )
            return f"An error occurred: {str(e)}"

    def _list_root_folder(self):
        items = self._list_folder_contents(self.root_folder_id)
        return self._format_items(items)

    def _list_folder_contents(self, folder_id):
        results = (
            self.service.files()
            .list(
                q=f"'{folder_id}' in parents",
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType)",
            )
            .execute()
        )
        return results.get("files", [])

    def _format_items(self, items):
        if not items:
            return "No files or folders found in the root directory."
        formatted = ["Files and folders in root directory:"]
        for item in items:
            icon = (
                "📁" if item["mimeType"] == "application/vnd.google-apps.folder" else "📄"
            )
            formatted.append(f"{icon} {item['name']} (ID: {item['id']})")
        return "\n".join(formatted)

    async def _arun(self):
        return self._run()
