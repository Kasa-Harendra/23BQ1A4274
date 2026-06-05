import requests

from logging_middleware.config import *

def Log(stack, level, package, message):
    token_type, access_token = "Bearer", ACCESS_TOKEN
    headers = {"Authorization": token_type + " " + access_token}
    body = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message
    }
    
    response = requests.post(
        url= BASE_URL + "logs", 
        headers=headers, 
        json=body
    )
    
    return response.json()

if __name__ == "__main__":
    print(Log("backend", "debug", "middleware", "Logging working"))