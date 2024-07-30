# manual_run.py

import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from centaur_workspace.tools.google_drive.navigate import GoogleDriveNavigationTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Authenticate and setup the service
SCOPES = ["https://www.googleapis.com/auth/drive"]
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
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
    with open(token_path, "wb") as token:
        pickle.dump(creds, token)

service = build("drive", "v3", credentials=creds)

# Initialize GoogleDriveNavigationTool with root folder ID
navigation_tool = GoogleDriveNavigationTool(service=service)


def list_contents():
    result = navigation_tool._run("list")
    print(result)


def enter_folder(folder_name):
    result = navigation_tool._run("enter", folder_name)
    print(result)


def go_back():
    result = navigation_tool._run("back")
    print(result)


def main():
    print("Google Drive Navigation CLI")
    print("Commands: 'list', 'enter [folder_name]', 'back', 'exit'")

    while True:
        user_input = input("> ").strip().split(" ", 1)
        command = user_input[0].lower()

        if command == "list":
            list_contents()
        elif command == "enter" and len(user_input) > 1:
            enter_folder(user_input[1])
        elif command == "back":
            go_back()
        elif command == "exit":
            break
        else:
            print("Invalid command. Try 'list', 'enter [folder_name]', 'back', 'exit'.")


if __name__ == "__main__":
    main()
