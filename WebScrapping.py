import requests
from bs4 import BeautifulSoup

def read_page(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    print(soup)

def page_links(url, match):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    links = set()
    for link in soup.findAll('a', href=True):
        sublink = link.get('href')
        if match in sublink and 'cpt-modifiers' not in sublink:
            links.add(sublink)
    return list(sorted(links))

def page_num_links(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    links = set()
    for link in soup.findAll('div', {'class':'col-md-12 pgbox'}):
        page_link = link.findAll('a', href=True)
        [links.add(p['href']) for p in page_link]
    return list(sorted(links))

# get links from first page
global url
url = 'https://www.aapc.com/codes/cpt-codes-range/'
sublinks = page_links(url, 'cpt-codes-range')

# get page link for all links from first page
for link in sublinks:
    print(link)
    page_nums = page_num_links(link)
    if page_nums != []:
        print(page_nums)

level1_links = list(set(sublinks))
print(level1_links)