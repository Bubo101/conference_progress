from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests
import json


def get_photo(city, state):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "per_page": 1,
        "query": city + " " + state,
    }
    # use params instead!
    # url = (
    #     "https://api.pexels.com/v1/search?query="
    #     + str(city)
    #     + ","
    #     + str(state)
    # )
    url = "https://api.pexels.com/v1/search"
    r = requests.get(url=url, headers=headers, params=params)
    photo = json.loads(r.content)
    try:
        return {"picture_url": photo["photos"][0]["src"]["original"]}
    except (KeyError, IndexError):
        return {"picture_url": None}


def get_weather_data(city, state):
    headers = {"Authorization": OPEN_WEATHER_API_KEY}
    params = {
        "q": f"{city}, {state}, US",
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,
    }
    # use params instead!
    # url = (
    #     "http://api.openweathermap.org/geo/1.0/direct?q="
    #     + str(city)
    #     + ","
    #     + str(state)
    #     + ","
    #     + "840&limit=1&appid="
    #     + OPEN_WEATHER_API_KEY
    # )
    url = "http://api.openweathermap.org/geo/1.0/direct"
    r = requests.get(url=url, headers=headers, params=params)
    weather = json.loads(r.content)
    try:
        lat = weather[0]["lat"]
        lon = weather[0]["lon"]
    except (KeyError, IndexError):
        return None

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }

    url = "https://api.openweathermap.org/data/2.5/weather"

    # use params instead!
    # url = (
    #     "https://api.openweathermap.org/data/2.5/weather?lat="
    #     + str(lat)
    #     + "&lon="
    #     + str(lon)
    #     + "&appid="
    #     + OPEN_WEATHER_API_KEY
    # )

    r = requests.get(url=url, headers=headers, params=params)
    weather_data = json.loads(r.content)

    try:
        return {
            "description": weather_data["weather"][0]["description"],
            "temp": weather_data["main"]["temp"],
        }
    except (KeyError, IndexError):
        return None
