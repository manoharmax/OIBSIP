from datetime import datetime, timezone
import requests
from config import API_KEY, BASE_URL


def get_weather(city):
    try:

        response = requests.get(
            BASE_URL,
            params={
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }
        )

        if response.status_code != 200:
            return None

        data = response.json()

        # City timezone offset in seconds
        timezone_offset = data.get("timezone", 0)

        sunrise_time = datetime.fromtimestamp(
            data["sys"]["sunrise"],
            tz=timezone.utc
        )

        sunset_time = datetime.fromtimestamp(
            data["sys"]["sunset"],
            tz=timezone.utc
        )

        sunrise_time = sunrise_time.timestamp() + timezone_offset
        sunset_time = sunset_time.timestamp() + timezone_offset

        sunrise = datetime.fromtimestamp(
            sunrise_time
        ).strftime("%I:%M %p")

        sunset = datetime.fromtimestamp(
            sunset_time
        ).strftime("%I:%M %p")

        return {
            "city": data["name"],
            "country": data["sys"]["country"],

            "temperature": round(
                data["main"]["temp"], 1
            ),

            "feels_like": round(
                data["main"]["feels_like"], 1
            ),

            "temp_min": round(
                data["main"]["temp_min"], 1
            ),

            "temp_max": round(
                data["main"]["temp_max"], 1
            ),

            "humidity": data["main"]["humidity"],

            "pressure": data["main"]["pressure"],

            "wind_speed": round(
                data["wind"]["speed"], 1
            ),

            "visibility": round(
                data["visibility"] / 1000, 1
            ),

            "clouds": data["clouds"]["all"],

            "sunrise": sunrise,
            "sunset": sunset,

            "description": data["weather"][0]["description"].title(),

            "icon": data["weather"][0]["icon"],
            
            "lat": data["coord"]["lat"],
            
            "lon": data["coord"]["lon"]
        }

    except Exception as e:
        print("Weather Service Error: - weather_service.py:94", e)
        return None