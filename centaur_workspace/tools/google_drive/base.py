import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import logging
from crewai_tools import BaseTool
from pydantic import Field
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive"]


class GoogleDriveBaseTool(BaseTool):
    service: Any = Field(default=None, exclude=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.service = self._get_drive_service()

    def _get_drive_service(self):
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
        return build("drive", "v3", credentials=creds)

    async def _arun(self, *args, **kwargs):
        return self._run(*args, **kwargs)
