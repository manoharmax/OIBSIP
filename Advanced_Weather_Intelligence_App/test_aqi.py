import requests
from config import API_KEY

lat = 16.9891
lon = 82.2475

url = (
    f"https://api.openweathermap.org/data/2.5/air_pollution"
    f"?lat={lat}&lon={lon}&appid={API_KEY}"
)

response = requests.get(url)

print(response.status_code)
print(response.json())