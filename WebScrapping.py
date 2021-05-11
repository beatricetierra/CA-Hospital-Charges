from bs4 import BeautifulSoup
import requests

URL = "https://www.aapc.com/codes/cpt-codes-range/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
html = soup.contents
for i in html:
    print(i)