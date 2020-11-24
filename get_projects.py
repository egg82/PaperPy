import requests
import time

from settings import GET_HEADERS

from utils import get_text

def main():
    response = get_response()
    if response is None:
        print("Could not get response!")
        return
    
    projects = response["projects"]
    for project in projects:
        print("Got project: " + project)

def get_response():
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

if __name__ == "__main__":
    main()