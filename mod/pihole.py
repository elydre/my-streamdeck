import requests
import urllib3
import json
import os

urllib3.disable_warnings()

pihole_url = None
api_key = None
sid = None

def read_config():
    global pihole_url, api_key

    if pihole_url is not None and api_key is not None:
        return True

    try:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../conf/conf.json")) as f:
            data = json.load(f)
            pihole_url = data["pihole_url"]
            api_key = data["pihole_key"]
    except:
        return False

    return pihole_url is not None and api_key is not None

def new_sid():
    response = requests.request("POST", f"{pihole_url}/auth", json = {"password": api_key}, verify = False)

    try:
        sid = response.json()["session"]["sid"]
        print(f"Got sid {sid}")
        return sid
    except:
        print("Failed to get sid")
        exit()

def get_from_api(path):
    global sid

    for i in range(2):
        if (sid is None):
            sid = new_sid()

        response = requests.request("GET", f"{pihole_url}/{path}?sid={sid}", verify = False)

        try:
            if (response.json()["error"]["key"]):
                sid = None
                continue
        except KeyError:
            pass

        if (response.status_code != 200):
            return None
        return response.json()

    return None

def show_info():
    if not read_config():
        return "check\nthe\nconfig"

    data = get_from_api("stats/summary")
    if data is None:
        return "get Error"

    try:
        return f"Pi-Hole\n{data['queries']['total']}\n" + (f"{float(data['queries']['percent_blocked']):.1f}%")
    except KeyError:
        return "parse Error"
