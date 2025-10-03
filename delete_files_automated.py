import os
import sys
import shutil
import json
import time
def print_status(status, file_name, project, site_name, info):
    status_message = {
        "status": status,
        "file_name": file_name,
        "project": project,
        "site_name": site_name,
        "info": info
    }
    time.sleep(1)
    json_message = json.dumps(status_message, indent=4)
    print(json_message)

def delete_project_files(base_path, project_name, site_name):
    project_path = os.path.join(base_path, project_name)

    if not os.path.exists(project_path):
        print_status("error", project_path, project_name, site_name, "Project path does not exist")
        return

    py_file_path = os.path.join(project_path, f"{site_name}_{project_name}.py")
    yml_file_path = os.path.join(project_path, f"{site_name}_{project_name}.yml")

    if os.path.exists(py_file_path):
        os.remove(py_file_path)
        print_status("deleted", py_file_path, project_name, site_name, "Python file deleted")

    if os.path.exists(yml_file_path):
        os.remove(yml_file_path)
        print_status("deleted", yml_file_path, project_name, site_name, "YAML file deleted")

    if not os.listdir(project_path):
        os.rmdir(project_path)
        print_status("deleted", project_path, project_name, site_name, "Empty project directory deleted")

def delete_text_file(base_path, project_name, site_name):
    project_path = os.path.join(base_path, project_name)

    if not os.path.exists(project_path):
        print_status("error", project_path, project_name, site_name, "Project path does not exist")
        return

    txt_file_path = os.path.join(project_path, f"{site_name}_{project_name}.txt")

    if os.path.exists(txt_file_path):
        os.remove(txt_file_path)
        print_status("deleted", txt_file_path, project_name, site_name, "Text file deleted")

    if not os.listdir(project_path):
        os.rmdir(project_path)
        print_status("deleted", project_path, project_name, site_name, "Empty project directory deleted")

def delete_folder(base_path, project_name, site_name):
    project_path = os.path.join(base_path, project_name)

    if not os.path.exists(project_path):
        print_status("error", project_path, project_name, site_name, "Project path does not exist")
        return

    site_folder_path = os.path.join(project_path, f"{site_name}_{project_name}")

    if os.path.exists(site_folder_path) and os.path.isdir(site_folder_path):
        shutil.rmtree(site_folder_path)
        print_status("deleted", site_folder_path, project_name, site_name, "Site folder deleted")

    if not os.listdir(project_path):
        os.rmdir(project_path)
        print_status("deleted", project_path, project_name, site_name, "Empty project directory deleted")

def delete_excel_file(base_path, project_name, site_name):
    project_path = os.path.join(base_path, project_name)

    if not os.path.exists(project_path):
        print_status("error", project_path, project_name, site_name, "Project path does not exist")
        return

    excel_file_path = os.path.join(project_path, f"{site_name}_{project_name}.xlsx")

    if os.path.exists(excel_file_path):
        os.remove(excel_file_path)
        print_status("deleted", excel_file_path, project_name, site_name, "Excel file deleted")

    if not os.listdir(project_path):
        os.rmdir(project_path)
        print_status("deleted", project_path, project_name, site_name, "Empty project directory deleted")

def main():
    if len(sys.argv) != 3:
        print("Usage: python delete_script.py <project_name> <site_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    site_name = sys.argv[2]

    base_dir = os.getcwd()

    url_collector_path = os.path.join(base_dir, 'url_collector')
    url_fetcher_path = os.path.join(base_dir, 'url_fetcher')
    url_extractor_path = os.path.join(base_dir, 'url_data_extractor')
    scrape_output_path = os.path.join(base_dir, 'scrape_output')

    delete_project_files(url_collector_path, project_name, site_name)
    delete_project_files(url_fetcher_path, project_name, site_name)
    delete_project_files(url_extractor_path, project_name, site_name)

    scrape_collector_output = os.path.join(scrape_output_path, 'collector_output')
    scrape_fetcher_output = os.path.join(scrape_output_path, 'fetcher_output')
    scrape_extractor_output = os.path.join(scrape_output_path, 'extractor_output')

    delete_text_file(scrape_collector_output, project_name, site_name)
    delete_folder(scrape_fetcher_output, project_name, site_name)
    delete_excel_file(scrape_extractor_output, project_name, site_name)

if __name__ == "__main__":
    main()