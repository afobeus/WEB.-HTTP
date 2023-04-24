import requests
from PIL import Image
from io import BytesIO
import sys
from distance import lonlat_distance

api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

address = " ".join(sys.argv[1:])

geocode_url = "https://geocode-maps.yandex.ru/1.x/"
geocode_params = {"geocode": address, "apikey": api_key, "format": "json"}
response = requests.get(geocode_url, params=geocode_params)
response_json = response.json()

pos = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")
latitude = pos[1]
longitude = pos[0]

search_url = "https://search-maps.yandex.ru/v1/"
search_params = {"apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3", "text": "аптека",
                 "ll": f"{longitude},{latitude}", "spn": "0.01,0.01", "results": "1",
                 "type": "biz", "lang": "ru_RU"}
response = requests.get(search_url, params=search_params)
response_json = response.json()
result_pos = response_json["features"][0]["geometry"]["coordinates"]
result_latitude = result_pos[1]
result_longitude = result_pos[0]

static_map_url = "https://static-maps.yandex.ru/1.x/"
static_map_params = {"ll": f"{longitude},{latitude}",
                     "l": "map", "pt": f"{result_longitude},{result_latitude},pm2rdl~"
                                       f"{longitude},{latitude},ya_ru"}
response = requests.get(static_map_url, params=static_map_params)

full_address = response_json["features"][0]["properties"]["description"]
print(full_address)
name = response_json["features"][0]["properties"]["name"]
print(name)
open_time = response_json["features"][0]["properties"]["CompanyMetaData"]["Hours"]["text"]
print(open_time)
print(lonlat_distance((float(longitude), float(latitude)),
                      (float(result_longitude), float(result_latitude))))
Image.open(BytesIO(response.content)).show()
