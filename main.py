import requests
import sys

geocoder_api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
organisations_api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address = " ".join(sys.argv[1:])

geocode_url = "https://geocode-maps.yandex.ru/1.x/"
geocode_params = {"geocode": address, "apikey": geocoder_api_key, "format": "json"}
response = requests.get(geocode_url, params=geocode_params)
response_json = response.json()

pos = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")
longitude, latitude = pos

geocode_params = {"geocode": f"{longitude},{latitude}", "apikey": geocoder_api_key,
                  "format": "json", "kind": "district", "results": 1}
response = requests.get(geocode_url, params=geocode_params)
response_json = response.json()
geo_object = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
district = geo_object["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"][4]["name"]
print("район -", district)
