from geopy.geocoders import Nominatim
import os 
import csv

dataset = r"C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Chargemaster Dataset"
hospitals = os.listdir(dataset)

geolocator = Nominatim(user_agent="example app")
with open('Addresses.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for hospital in hospitals:
        try:
            location = geolocator.geocode(hospital)
            lat = location.raw['lat']
            lon = location.raw['lon']
        except:
            locations, lat, lon = 3*['N/A'] 
        writer.writerow([hospital, location, lat, lon])