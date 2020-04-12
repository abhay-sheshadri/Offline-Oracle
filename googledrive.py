from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import socket

# Authenticate the user
def auth():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

# Get a list of the files in the 'Offline Oracle Updates' folder in google drive
def get_files(drive):
    folder_id = '1arH7DVoP8CKSa7cwAdmoiOOQZp8II6B4'
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
    file_data = {}
    for file1 in file_list:
        file_data[file1['title']] = file1['id']
    return file_data

# Download a file from the 'Offline Oracle Updates' folder in google drive by file id
def download_file(file_id, file_name, drive):
    f = drive.CreateFile({"id": file_id})
    f.GetContentFile(os.path.abspath("updates/"+file_name))

# Downloads the list of files which are in the google drive but not the folder.  Will return a list of file paths
def get_different(drive):
    # google drive file names and ids
    drive_data = get_files(drive)
    drive_names = set(drive_data.keys())
    # Files in folder names
    folder_names = set(os.listdir(os.path.abspath("updates")))
    # Get difference
    fpaths = []
    for f in folder_names.symmetric_difference(drive_names):
        f_id = drive_data[f]
        download_file(f_id, f, drive)
        fpaths.append(os.path.abspath("updates/"+f))
    return fpaths

# Checks if there is an internet connection present
def check_internet():
    try:
        # tests connection to google.com
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False



# get_different(auth())