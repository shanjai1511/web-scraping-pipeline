import os

def list_folders(directory, exclude_folders=None):
    if exclude_folders is None:
        exclude_folders = []

    for root, dirs, files in os.walk(directory):
        # Filter out excluded folders
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        
        # Print the remaining folders
        for d in dirs:
            print(os.path.join(root, d))

# Specify the directory you want to list folders from
directory_to_search = r"C:\Users\shanj\OneDrive\Desktop\web-scrapping-pipeline"

# Specify the folders you want to exclude
exclude_folders = ['__pycache__', 'myenv','.git']

# Call the function
list_folders(directory_to_search, exclude_folders)

#create new branch - git checkout -b temp$(Get-Date -Format "yyyyMMddHHmmss")