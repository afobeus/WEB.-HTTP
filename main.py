import random
from io import BytesIO

import requests
from PIL import Image

geocoder_api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

cities = ["Санкт-Петербург", "Ванкувер", "Нью-Йорк", "Париж", "Мадрид", "Белград"]
cities_cords = []
for city in cities:
    geocode_url = "https://geocode-maps.yandex.ru/1.x/"
    geocode_params = {"geocode": city, "apikey": geocoder_api_key, "format": "json"}
    response = requests.get(geocode_url, params=geocode_params)
    response_json = response.json()
    pos = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")
    cities_cords.append(pos)

while True:
    cords_index = random.randint(0, len(cities_cords) - 1)
    longitude, latitude = cities_cords[cords_index]
    map_type = random.choice(["map", "sat"])
    static_map_url = "https://static-maps.yandex.ru/1.x/"
    static_map_params = {"ll": f"{longitude},{latitude}", "l": map_type, "z": 14}
    response = requests.get(static_map_url, params=static_map_params)
    Image.open(BytesIO(response.content)).show()
    print("Для показа следующего слайда нажмите Enter")
    input()
