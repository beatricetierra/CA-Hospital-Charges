import requests
from bs4 import BeautifulSoup
import csv

def category1():
    anesthesia = list(map(lambda n: "{:05d}".format(n), range(100,1999)))
    surgery = [str(n) for n in range(10004,69990)]
    radiology = [str(n) for n in range(70010,79999)]
    lab = list(map(lambda n: "{:04d}U".format(n), range(1,247)))
    pathology = [str(n) for n in range(80047,89398)]
    medicine = [str(n) for n in range(90281,99607)]
    evaluation = [str(n) for n in range(99091,99499)]
    category1 =  anesthesia + surgery + radiology + \
                lab + pathology + medicine + evaluation
    return list(set(category1))

def category2():
    l = map(lambda n: "{:04d}F".format(n), range(1,9007))
    return list(l)

def category3():
    l = map(lambda n: "{:04d}T".format(n), range(42,639))
    return list(l)

# combine all category cpt codes
cpt_numbers = category2() + category3()
cpt_links = list(map(lambda num: "https://www.aapc.com/codes/cpt-codes/" + num, cpt_numbers))

with open('CPTCodes_AAPC(2) .csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Code Number', 'Summary'])
    for num, url in zip(cpt_numbers, cpt_links):
        req = requests.get(url)
        if req.status_code == 200:
            try:
                soup = BeautifulSoup(req.content, 'html.parser')
                desc = soup.find('div', {'id':"cpt_layterms"})
                summary = desc.find('p').text
            except:
                summary = 'N/A'
            writer.writerow([num, summary])