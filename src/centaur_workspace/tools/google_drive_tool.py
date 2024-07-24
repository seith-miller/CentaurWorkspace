import os
import pickle
import io
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from crewai_tools import BaseTool

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class GoogleDriveTool(BaseTool):
    name: str = "Google Drive Tool"
    description: str = (
        "A tool that reads and writes content from/to Google Drive files."
    )

    def _get_credentials(self):
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return creds

    def _run(self, action: str, file_id: str, content: str = None) -> str:
        """Perform actions on Google Drive files."""
        creds = self._get_credentials()
        service = build("drive", "v3", credentials=creds)

        if action == "read":
            return self._read_file(service, file_id)
        elif action == "write":
            return self._write_file(service, file_id, content)
        else:
            return "Invalid action. Use 'read' or 'write'."

    def _read_file(self, service, file_id):
        file = service.files().get(fileId=file_id).execute()
        mime_type = file["mimeType"]

        if mime_type == "application/vnd.google-apps.document":
            # Google Doc
            docs_service = build("docs", "v1", credentials=service._credentials)
            doc = docs_service.documents().get(documentId=file_id).execute()
            return self._extract_text_from_doc(doc)
        elif mime_type == "application/vnd.google-apps.spreadsheet":
            # Google Sheet
            sheets_service = build("sheets", "v4", credentials=service._credentials)
            sheet = sheets_service.spreadsheets().get(spreadsheetId=file_id).execute()
            return self._extract_text_from_sheet(sheets_service, file_id, sheet)
        else:
            # Other file types (including PDF)
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            return fh.getvalue().decode("utf-8")

    def _write_file(self, service, file_id, content):
        file = service.files().get(fileId=file_id).execute()
        mime_type = file["mimeType"]

        if mime_type == "application/vnd.google-apps.document":
            # Google Doc
            docs_service = build("docs", "v1", credentials=service._credentials)
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
            docs_service.documents().batchUpdate(
                documentId=file_id, body={"requests": requests}
            ).execute()
        elif mime_type == "application/vnd.google-apps.spreadsheet":
            # Google Sheet
            sheets_service = build("sheets", "v4", credentials=service._credentials)
            body = {"values": [[content]]}
            sheets_service.spreadsheets().values().update(
                spreadsheetId=file_id,
                range="Sheet1!A1",
                valueInputOption="RAW",
                body=body,
            ).execute()
        else:
            # Other file types (including PDF) - cannot be updated directly
            return "Writing to this file type is not supported."

        return f"Content written to file {file_id}"

    def _extract_text_from_doc(self, doc):
        text = []
        for elem in doc.get("body").get("content"):
            if "paragraph" in elem:
                for para_elem in elem["paragraph"]["elements"]:
                    if "textRun" in para_elem:
                        text.append(para_elem["textRun"]["content"])
        return "".join(text)

    def _extract_text_from_sheet(self, sheets_service, spreadsheet_id, sheet):
        result = (
            sheets_service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range="Sheet1")
            .execute()
        )
        rows = result.get("values", [])
        return "\n".join(["\t".join(row) for row in rows])

    async def _arun(self, action: str, file_id: str, content: str = None) -> str:
        """Asynchronous version of _run."""
        return self._run(action, file_id, content)
