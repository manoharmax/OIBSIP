import json
import os

FILE_NAME = "search_history.json"


def load_history():

    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except:
        return []


def save_city(city):

    history = load_history()

    city = city.title()

    if city in history:
        history.remove(city)

    history.insert(0, city)

    history = history[:5]

    with open(FILE_NAME, "w") as file:
        json.dump(history, file, indent=4)

    return history