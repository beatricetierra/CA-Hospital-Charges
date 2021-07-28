from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re
import csv

# url = "https://www.ahd.com/states/hospital_CA.html"
# html = urlopen(url).read()
# bs = BeautifulSoup(html, features="lxml")
# table = bs.find(lambda tag: tag.name=='table')
# extensions = []
# for anchor in table.findAll('tr'):
#     cell = anchor.find('a', href=True)
#     extension = re.findall('"([^"]*)"', str(cell))
#     extensions.extend(extension)

# home_page = "https://www.ahd.com"
# hospital_profiles = [home_page + extension for extension in extensions]

# with open('HospitalTable.csv', 'w', newline='') as file:
#     for hospital in hospital_profiles:
#         writer = csv.writer(file)
#         writer.writerow([hospital])

import pandas as pd
df = pd.read_csv('HospitalTable.csv')
series = df.iloc[:,0]
for profile in series:
    print(profile)
    html = urlopen(profile).read()
    bs = BeautifulSoup(html, features="lxml")
    table = bs.find('table', "noborder nomargin")
    print(table)