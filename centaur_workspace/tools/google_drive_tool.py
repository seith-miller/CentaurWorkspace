import io
import os
import pickle
from crewai_tools import BaseTool
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

SCOPES = ["https://www.googleapis.com/auth/drive"]

# Load environment variables
load_dotenv()


class GoogleDriveBaseTool(BaseTool):
    def _get_credentials(self):
        creds = None
        token_path = "token.pickle"
        credentials_path = "credentials.json"

        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(token_path, "wb") as token:
                pickle.dump(creds, token)

        return creds


class GoogleDriveListTool(GoogleDriveBaseTool):
    name: str = "Google Drive List Tool"
    description: str = "Lists files in a specific folder in your Google Drive."

    def _run(self) -> str:
        try:
            folder_id = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID")
            if not folder_id:
                return "Root folder ID is not set in the environment variables."

            creds = self._get_credentials()
            service = build("drive", "v3", credentials=creds)
            query = f"'{folder_id}' in parents"
            results = (
                service.files()
                .list(
                    q=query,
                    pageSize=10,
                    fields="nextPageToken, files(id, name, mimeType)",
                )
                .execute()
            )
            items = results.get("files", [])
            if not items:
                return "No files found in the specified folder."
            return "\n".join(
                [
                    f"{item['name']} ({item['id']}) - {item['mimeType']}"
                    for item in items
                ]
            )
        except Exception as e:
            return f"An error occurred: {str(e)}"


class GoogleDriveReadTool(GoogleDriveBaseTool):
    name: str = "Google Drive Read Tool"
    description: str = (
        "Reads the content of a specific file in your Google Drive. "
        "Provide the file_id as input."
    )

    def _run(self, file_id: str) -> str:
        try:
            creds = self._get_credentials()
            service = build("drive", "v3", credentials=creds)
            file = service.files().get(fileId=file_id, fields="mimeType").execute()
            mime_type = file["mimeType"]

            if mime_type == "application/vnd.google-apps.document":
                docs_service = build("docs", "v1", credentials=creds)
                doc = docs_service.documents().get(documentId=file_id).execute()
                return self._extract_text_from_doc(doc)
            else:
                request = service.files().get_media(fileId=file_id)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                return fh.getvalue().decode("utf-8")
        except Exception as e:
            return f"An error occurred while reading the file: {str(e)}"

    def _extract_text_from_doc(self, doc):
        text = []
        for elem in doc.get("body", {}).get("content", []):
            if "paragraph" in elem:
                for para_elem in elem["paragraph"].get("elements", []):
                    if "textRun" in para_elem:
                        text.append(para_elem["textRun"]["content"])
        return "".join(text)


class GoogleDriveWriteTool(GoogleDriveBaseTool):
    name: str = "Google Drive Write Tool"
    description: str = (
        "Writes content to a specific file in your Google Drive. "
        "Provide the file_id and content as input."
    )

    def _run(self, file_id: str, content: str) -> str:
        try:
            creds = self._get_credentials()
            service = build("drive", "v3", credentials=creds)
            file = service.files().get(fileId=file_id, fields="mimeType").execute()
            mime_type = file["mimeType"]

            if mime_type == "application/vnd.google-apps.document":
                docs_service = build("docs", "v1", credentials=creds)
                requests = [{"insertText": {"location": {"index": 1}, "text": content}}]
                docs_service.documents().batchUpdate(
                    documentId=file_id, body={"requests": requests}
                ).execute()
                return f"Content written to file {file_id}"
            else:
                return "Writing to this file type is not supported."
        except Exception as e:
            return f"An error occurred while writing to the file: {str(e)}"
