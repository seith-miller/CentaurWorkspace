from .base import GoogleDriveBaseTool, logger
from googleapiclient.http import MediaIoBaseUpload
import io


class GoogleDriveWriteTool(GoogleDriveBaseTool):
    name: str = "Google Drive Write Tool"
    description: str = "Write or update contents of a file in Google Drive"

    def _run(self, file_id: str, content: str):
        try:
            file = self.service.files().get(fileId=file_id, fields="mimeType").execute()
            mime_type = file["mimeType"]

            if mime_type == "application/vnd.google-apps.document":
                return self._update_google_doc(file_id, content)
            else:
                return self._update_regular_file(file_id, content, mime_type)
        except Exception as e:
            logger.error(f"An error occurred while writing to the file: {str(e)}")
            return f"An error occurred while writing to the file: {str(e)}"

    def _update_google_doc(self, file_id, content):
        requests = [
            {
                "insertText": {
                    "location": {
                        "index": 1,
                    },
                    "text": content,
                }
            }
        ]
        self.service.documents().batchUpdate(
            documentId=file_id, body={"requests": requests}
        ).execute()
        return f"Content written to Google Doc with ID: {file_id}"

    def _update_regular_file(self, file_id, content, mime_type):
        media = MediaIoBaseUpload(
            io.BytesIO(content.encode()), mimetype=mime_type, resumable=True
        )
        self.service.files().update(fileId=file_id, media_body=media).execute()
        return f"Content written to file with ID: {file_id}"
