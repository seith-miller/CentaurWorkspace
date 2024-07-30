from .base import GoogleDriveBaseTool, logger
from googleapiclient.http import MediaIoBaseUpload
import io


class GoogleDriveCreateTool(GoogleDriveBaseTool):
    name: str = "Google Drive Create Tool"
    description: str = "Create a new file or folder in Google Drive"

    def _run(
        self, name: str, mime_type: str, parent_id: str = None, content: str = None
    ):
        try:
            file_metadata = {"name": name, "mimeType": mime_type}
            if parent_id:
                file_metadata["parents"] = [parent_id]

            if mime_type == "application/vnd.google-apps.folder":
                file = (
                    self.service.files()
                    .create(body=file_metadata, fields="id")
                    .execute()
                )
                return f"Folder created with ID: {file.get('id')}"
            else:
                if content is None:
                    content = ""
                media = MediaIoBaseUpload(
                    io.BytesIO(content.encode()), mimetype=mime_type, resumable=True
                )
                file = (
                    self.service.files()
                    .create(body=file_metadata, media_body=media, fields="id")
                    .execute()
                )
                return f"File created with ID: {file.get('id')}"
        except Exception as e:
            logger.error(f"An error occurred while creating the file/folder: {str(e)}")
            return f"An error occurred while creating the file/folder: {str(e)}"
