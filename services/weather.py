import requests

API_KEY = "OPENWEATHER_API_KEY"  # set trong ENV
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "vi"
    }
    r = requests.get(BASE_URL, params=params, timeout=10)
    if r.status_code != 200:
        return None

    d = r.json()
    return {
        "city": d["name"],
        "temp": d["main"]["temp"],
        "desc": d["weather"][0]["description"],
        "hum": d["main"]["humidity"]
    }
