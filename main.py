import requests
from PIL import Image
from io import BytesIO
import sys
from distance import lonlat_distance

geocoder_api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
organisations_api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address = " ".join(sys.argv[1:])

geocode_url = "https://geocode-maps.yandex.ru/1.x/"
geocode_params = {"geocode": address, "apikey": geocoder_api_key, "format": "json"}
response = requests.get(geocode_url, params=geocode_params)
response_json = response.json()

pos = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")
latitude = pos[1]
longitude = pos[0]

search_url = "https://search-maps.yandex.ru/v1/"
search_params = {"apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3", "text": "аптека",
                 "ll": f"{longitude},{latitude}", "spn": "0.01,0.01", "results": "10",
                 "type": "biz", "lang": "ru_RU"}
response = requests.get(search_url, params=search_params)
response_json = response.json()
result_points = []
for elem in response_json["features"]:
    cords = list(map(str, elem["geometry"]["coordinates"]))
    if "Hours" in elem["properties"]["CompanyMetaData"]:
        hours = elem["properties"]["CompanyMetaData"]["Hours"]
        if "TwentyFourHours" in hours["Availabilities"][0]:
            result_points.append((*cords, "pm2gnm"))  # pm2gnm - medium green point
        else:
            result_points.append((*cords, "pm2blm"))  # pm2blm - medium blue point
    else:
        result_points.append((*cords, "pm2grm"))  # pm2grm - medium gray point

static_map_url = "https://static-maps.yandex.ru/1.x/"
static_map_params = {"ll": f"{longitude},{latitude}", "l": "map",
                     "pt": '~'.join(','.join(elem) for elem in result_points)}
response = requests.get(static_map_url, params=static_map_params)
Image.open(BytesIO(response.content)).show()
