import requests
from config import Config


def get_address_details(address):
    api_key = Config.GOOGLE_MAPS_API_KEY
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': address,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            address_components = data['results'][0]['address_components']

            lat = location['lat']
            lng = location['lng']
            city = None
            department = None
            country = None

            for component in address_components:
                if 'locality' in component['types']:
                    city = component['long_name']
                if 'administrative_area_level_1' in component['types']:
                    department = component['long_name']
                if 'country' in component['types']:
                    country = component['long_name']

            return lat, lng, city, department, country
    return None, None, None, None, None
