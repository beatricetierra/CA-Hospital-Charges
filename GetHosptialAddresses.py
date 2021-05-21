import config
import requests
import json
import csv
import os

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
        return results

dataset = r"C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Datasets\Chargemaster Dataset"
hospitals = os.listdir(dataset)

places = GooglePlaces(config.api_key)

with open('Addresses2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Hospital', 'Address', 'Latitude', 'Longitude'])
    for hospital in hospitals:
        try:
            results = places.get_address(hospital)
            address = results['formatted_address']
            lat = results['geometry']['location']['lat']
            lng = results['geometry']['location']['lng']
            print(lat, lng)
        except:
            address, lat, lng = 3*['N/A'] 
        writer.writerow([hospital, address, lat, lng])
        

