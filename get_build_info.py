import requests
import time

from settings import GET_HEADERS

from utils import get_text

def main():
    response = get_response("paper", "1.12.2", 1618)
    if response is None:
        print("Could not get response!")
        return
    
    print("Project ID: " + response["project_id"])
    print("Project name: " + response["project_name"])
    print("Version: " + response["version"])
    print("Build: " + str(response["build"]))
    print("Time: " + response["time"])

    for change in response["changes"]:
        print("Commit: " + change["commit"])
        print("Summary: " + change["summary"])
        print("Message: " + change["message"])
    for download_name, download_data in response["downloads"].items():
        print("Download: " + download_name)
        print("Name: " + download_data["name"])
        print("SHA256: " + download_data["sha256"])

def get_response(project, version, build):
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

if __name__ == "__main__":
    main()