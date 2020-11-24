import requests
import time
import hashlib

from settings import GET_HEADERS
from settings import GET_DATA_HEADERS

from utils import get_text

def main():
    projects = get_projects()
    if projects is None:
        print("Could not get projects!")
        return
    
    for project in projects["projects"]:
        project_info = get_project_info(project)
        if project_info is None:
            print("Could not get project info for " + project)
            continue
        
        latest_version = project_info["versions"][-1]
        version_info = get_version_info(project, latest_version)
        if version_info is None:
            print("Could not get version info for " + project + " " + latest_version)
            continue

        latest_build = version_info["builds"][-1]
        build_info = get_build_info(project, latest_version, latest_build)
        if build_info is None:
            print("Could not get build info for " + project + " " + latest_version + " (" + str(latest_build) + ")")
            continue

        for download_name, download_data in build_info["downloads"].items():
            if download_name == "application":
                response = get_download(project, latest_version, latest_build, download_data["name"])
                if response is None:
                    print("Could not get file response!")
                    return
                
                with open(project + ".jar", "wb") as out_file:
                    out_file.write(response)
                
                with open(project + ".jar", "rb") as file_bytes:
                    sha256 = hashlib.sha256()
                    sha256.update(file_bytes.read())
                    if not sha256.hexdigest() == download_data["sha256"]:
                        print("Downloaded file hash for " + project + " does not match! Please re-try the download.")
                    else:
                        print(project + " successfully downloaded!")

def get_projects():
    global GET_HEADERS

    tries = 0
    while True:
        req = requests.get("https://papermc.io/api/v2/projects", headers=GET_HEADERS)
        if req.status_code == 429:
            time.sleep(0.5)
        else:
            ret_val = get_text(req)
            if not ret_val is None:
                return ret_val
            elif ret_val is None and tries >= 3:
                return ret_val
            else:
                tries += 1
                time.sleep(3.0)

def get_project_info(project):
    global GET_HEADERS

    tries = 0
    while True:
        req = requests.get("https://papermc.io/api/v2/projects/" + project, headers=GET_HEADERS)
        if req.status_code == 429:
            time.sleep(0.5)
        else:
            ret_val = get_text(req)
            if not ret_val is None:
                return ret_val
            elif ret_val is None and tries >= 3:
                return ret_val
            else:
                tries += 1
                time.sleep(3.0)

def get_version_info(project, version):
    global GET_HEADERS

    tries = 0
    while True:
        req = requests.get("https://papermc.io/api/v2/projects/" + project + "/versions/" + version, headers=GET_HEADERS)
        if req.status_code == 429:
            time.sleep(0.5)
        else:
            ret_val = get_text(req)
            if not ret_val is None:
                return ret_val
            elif ret_val is None and tries >= 3:
                return ret_val
            else:
                tries += 1
                time.sleep(3.0)

def get_build_info(project, version, build):
    global GET_HEADERS

    tries = 0
    while True:
        req = requests.get("https://papermc.io/api/v2/projects/" + project + "/versions/" + version + "/builds/" + str(build), headers=GET_HEADERS)
        if req.status_code == 429:
            time.sleep(0.5)
        else:
            ret_val = get_text(req)
            if not ret_val is None:
                return ret_val
            elif ret_val is None and tries >= 3:
                return ret_val
            else:
                tries += 1
                time.sleep(3.0)

def get_download(project, version, build, download):
    global GET_DATA_HEADERS

    tries = 0
    while True:
        req = requests.get("https://papermc.io/api/v2/projects/" + project + "/versions/" + version + "/builds/" + str(build) + "/downloads/" + download, headers=GET_DATA_HEADERS)
        if req.status_code == 429:
            time.sleep(0.5)
        else:
            ret_val = req.content
            if not ret_val is None:
                return ret_val
            elif ret_val is None and tries >= 3:
                return ret_val
            else:
                tries += 1
                time.sleep(3.0)

if __name__ == "__main__":
    main()