import requests
from config import API_KEY


def get_aqi(lat, lon):

    url = "https://api.openweathermap.org/data/2.5/air_pollution"

    response = requests.get(
        url,
        params={
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        }
    )

    if response.status_code != 200:
        return None

    data = response.json()

    item = data["list"][0]

    aqi_value = item["main"]["aqi"]

    aqi_labels = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }

    return {
        "aqi": aqi_value,
        "label": aqi_labels.get(aqi_value, "Unknown"),

        "pm25": round(item["components"]["pm2_5"], 2),
        "pm10": round(item["components"]["pm10"], 2),

        "co": round(item["components"]["co"], 2),
        "no2": round(item["components"]["no2"], 2),
        "o3": round(item["components"]["o3"], 2)
    }