from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import socket, os

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# Gets the google drive api service
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)
service = build('drive', 'v3', credentials=creds)

# Checks if there is an internet connection present
def check_internet():
    try:
        # tests connection to google.com
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

# Get filenames and ids from the folder
def get_names_and_ids():
    results = service.files().list(
        pageSize=size,
        fields="nextPageToken, files(id, name)"
    ).execute()


# uploads a file into google drive folder. Will be placed in the "Offline Oracle Updates" folder
def upload_file(file_path, file_name):
    file_path = os.path.abspath(file_path)
    file_metadata ={
        "name": file_name,
    }
    media = MediaFileUpload(file_path, mimetype="")
    f = service.files().create(body=file_metadata, media)

# Get file from google drive.  Must be in the "Offline Oracle Updates" folder.  Downloaded file will be placed in the updates folder.
def download_file(file_name):
    pass

