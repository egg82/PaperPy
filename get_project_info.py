import requests
import time

from settings import GET_HEADERS

from utils import get_text

def main():
    response = get_response("paper")
    if response is None:
        print("Could not get response!")
        return
    
    print("Project ID: " + response["project_id"])
    print("Project name: " + response["project_name"])
    for group in response["version_groups"]:
        print("Version group: " + group)
    for version in response["versions"]:
        print("Version: " + version)

def get_response(project):
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

if __name__ == "__main__":
    main()