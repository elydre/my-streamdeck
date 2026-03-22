import requests
import requests
import json
import os

weather_city = None

def read_config():
    global weather_city

    if weather_city is not None:
        return True

    try:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../conf/conf.json")) as f:
            data = json.load(f)
            weather_city = data["weather_city"]
    except:
        return False

    return isinstance(weather_city, str) and len(weather_city) > 0

winddir16_to_arrow = {
    "N": "↓",
    "NNE": "↓",
    "NE": "↙",
    "ENE": "←",
    "E": "←",
    "ESE": "←",
    "SE": "↖",
    "SSE": "↑",
    "S": "↑",
    "SSW": "↑",
    "SW": "↗",
    "WSW": "→",
    "W": "→",
    "WNW": "→",
    "NW": "↘",
    "NNW": "↓",
}

def get_weather():
    url = f"https://wttr.in/{weather_city}?format=j1"

    try:
        response = requests.get(url)
        data = response.json()

        return data["current_condition"][0]

    except Exception as e:
        return None

def render_weather(data):
    return f"{data['temp_C']}°C\n{data['humidity']}%\n{data['windspeedKmph']} km/h\n{data['winddir16Point']} {winddir16_to_arrow.get(data['winddir16Point'], '?')}"

def show_info():
    if not read_config():
        return "check\nthe\nconfig"

    data = get_weather()
    if data is None:
        return "get Error"
    
    try:
        return render_weather(data)
    except KeyError:
        return "parse Error"
