import requests
import time
import hashlib

from settings import GET_HEADERS
from settings import GET_DATA_HEADERS

from utils import get_text

def main():
    build_info = get_build_info("paper", "1.12.2", 1618)
    if build_info is None:
        print("Could not get build response!")
        return

    response = get_response("paper", "1.12.2", 1618, "paper-1.12.2-1618.jar")
    if response is None:
        print("Could not get file response!")
        return
    
    with open("paper-1.12.2-1618.jar", "wb") as out_file:
        out_file.write(response)
    
    with open("paper-1.12.2-1618.jar", "rb") as file_bytes:
        sha256 = hashlib.sha256()
        sha256.update(file_bytes.read())
        if not sha256.hexdigest() == build_info["downloads"]["application"]["sha256"]:
            print("Downloaded file hash does not match! Please re-try the download.")
        else:
            print("File successfully downloaded!")

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

def get_response(project, version, build, download):
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