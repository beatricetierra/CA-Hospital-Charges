import requests
import json
import time
class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey
 
    def get_address(self, name):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        places = []
        params = {
            'key': self.apiKey,
            'input': name,
            'inputtype': 'textquery',
            'fields' : 'formatted_address,name,geometry'
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)['candidates'][0]

        address = results['formatted_address']
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
        formal_name = results['name']
        print(formal_name, address, lat, lng)


places = GooglePlaces(hidden_key)
places.get_address('Unversity of California Irvine Medical Center')
