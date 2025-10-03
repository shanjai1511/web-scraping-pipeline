import os
import sys
from pydrive.auth import GoogleAuth #type: ignore
from pydrive.drive import GoogleDrive #type: ignore

class GoogleDriveUploader:
    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()  # Creates local webserver and handles authentication
        self.drive = GoogleDrive(self.gauth)
    
    def get_folder_id(self, folder_name):
        folder_list = self.drive.ListFile({'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder'"}).GetList()
        
        if folder_list:
            return folder_list[0]['id']
        else:
            raise FileNotFoundError(f"No folder found with the name '{folder_name}'")
    
    def file_exists(self, folder_id, file_name):
        file_list = self.drive.ListFile({'q': f"'{folder_id}' in parents and title='{file_name}'"}).GetList()
        return len(file_list) > 0
    
    def upload_file(self, local_file_path, drive_folder_id):
        file_name = os.path.basename(local_file_path)
        if not os.path.isfile(local_file_path):
            print(f"Error: The file '{file_name}' does not exist in the local folder.")
            return
        
        if self.file_exists(drive_folder_id, file_name):
            print(f"The file '{file_name}' already exists in the Google Drive folder.")
        else:
            upload_file = self.drive.CreateFile({
                'title': file_name,
                'parents': [{'id': drive_folder_id}]
            })
            upload_file.SetContentFile(local_file_path)
            upload_file.Upload()
            print(f'Uploaded file {file_name} with ID: {upload_file.get("id")}')
    
    def upload_files_from_folder(self, local_folder, drive_folder_name):
        try:
            drive_folder_id = self.get_folder_id(drive_folder_name)

            # Check if local folder exists
            if not os.path.isdir(local_folder):
                print(f"Error: The local folder '{local_folder}' does not exist.")
                return

            files_uploaded = False
            for file_name in os.listdir(local_folder):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(local_folder, file_name)
                    self.upload_file(file_path, drive_folder_id)
                    files_uploaded = True
            
            if not files_uploaded:
                print("No CSV files found in the local folder.")

        except FileNotFoundError as fnf_error:
            print(fnf_error)
        except Exception as e:
            print(f'An error occurred: {e}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <local_folder_path> <google_drive_folder_name>")
        sys.exit(1)
    project_name = sys.argv[1]
    local_folder = f"C:/Users/shanj/OneDrive/Desktop/web-scrapping-pipeline/scrape_output/extractor_output/{project_name}"
    drive_folder_name = project_name
    import pdb; pdb.set_trace()
    uploader = GoogleDriveUploader()
    uploader.upload_files_from_folder(local_folder, drive_folder_name)