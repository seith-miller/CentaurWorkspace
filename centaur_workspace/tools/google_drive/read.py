from .base import GoogleDriveBaseTool, logger


class GoogleDriveReadTool(GoogleDriveBaseTool):
    name: str = "Google Drive Read Tool"
    description: str = "Read contents of a file in Google Drive"

    def _run(self, file_name: str):
        try:
            logger.info(f"Attempting to read file: {file_name}")
            print(f"DEBUG: Attempting to read file: {file_name}")

            file_id = self._get_file_id(file_name)
            print(f"DEBUG: File ID retrieved: {file_id}")

            if not file_id:
                return f"File '{file_name}' not found."

            file_info = (
                self.service.files().get(fileId=file_id, fields="mimeType").execute()
            )
            mime_type = file_info.get("mimeType", "application/octet-stream")
            print(f"DEBUG: File mime type: {mime_type}")

            if mime_type == "application/vnd.google-apps.document":
                logger.info("Reading as Google Doc")
                content = self._read_google_doc(file_id)
            else:
                logger.info("Reading as regular file")
                content = self._read_regular_file(file_id)

            return content.decode("utf-8") if isinstance(content, bytes) else content
        except Exception as e:
            logger.error(
                f"An error occurred while reading the file: {str(e)}", exc_info=True
            )
            print(f"DEBUG: Error in _run: {str(e)}")
            return f"An error occurred while reading the file: {str(e)}"

    def _get_file_id(self, file_name: str):
        query = f"name = '{file_name}'"
        results = self.service.files().list(q=query, fields="files(id)").execute()
        files = results.get("files", [])
        return files[0]["id"] if files else None

    def _read_google_doc(self, file_id):
        return (
            self.service.files()
            .export_media(fileId=file_id, mimeType="text/plain")
            .execute()
        )

    def _read_regular_file(self, file_id):
        return self.service.files().get_media(fileId=file_id).execute()

    async def _arun(self, file_name: str):
        return self._run(file_name)
