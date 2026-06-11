import requests
from config import API_KEY


def get_forecast(lat, lon):

    url = "https://api.openweathermap.org/data/2.5/forecast"

    response = requests.get(
        url,
        params={
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"
        }
    )

    if response.status_code != 200:
        return None

    data = response.json()

    forecast = []
    used_dates = set()

    for item in data["list"]:

        date = item["dt_txt"].split(" ")[0]

        if date in used_dates:
            continue

        used_dates.add(date)

        forecast.append({
            "date": date,
            "temp": round(item["main"]["temp"]),
            "description": item["weather"][0]["main"]
        })

        if len(forecast) == 5:
            break

    return forecast