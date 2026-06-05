import requests
import sys 
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from logging_middleware.log import Log, get_access_token
from logging_middleware.config import *

def get_depots_data():
    headers = {"Authorization": ' '.join(get_access_token()).strip()}
    url = BASE_URL + "depots"
    response = requests.get(url=url, headers=headers)
    Log("backend", "info", "utils", "Getting depots data")
    return response.json()

def get_vehicles_data():
    headers = {"Authorization": ' '.join(get_access_token()).strip()}
    url = BASE_URL + "vehicles"
    response = requests.get(url=url, headers=headers)
    Log("backend", "info", "utils", "Getting vehicles data")
    return response.json()

# print(get_depots_data())