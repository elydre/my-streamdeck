import requests
import json
import os

pihole_url = None
api_key = None

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

def disable(time = 120):
    if not read_config():
        return
    try:
        requests.get(pihole_url, params={"auth": api_key, "disable": time})
    except:
        pass

def show_info():
    if not read_config():
        return "check\nthe\nconfig"
    
    try:
        response = requests.get(pihole_url, params={"auth": api_key, "summaryRaw": ""})
        data = response.json()

        return f"Pi-Hole\n{data['dns_queries_today']}\n" + (f"{float(data['ads_percentage_today']):.1f}%" if data["status"] == "enabled" else "OFF")
    except:
        return "Error"
