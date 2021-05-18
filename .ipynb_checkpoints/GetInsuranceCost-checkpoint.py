import re
import pandas as pd
import csv
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

# 1. Get zip codes
csv_file = r'C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Datasets\Addresses.csv'
address_df = pd.read_csv(csv_file)
zipcodes = [re.search('CA \d\d\d\d\d', add).group(0).split(' ')[1] for add in address_df['Address']]

# 2. Get proxy list
req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
proxies = req_proxy.get_proxy_list() #this will create proxy list

# 3. Get cost after insurance 
codes = ['99282', '99283', '99284', '99285']
with open('CoverageCost.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['CPT Code', 'Zip', 'In-Network', 'Out-Network'])
    for i, code in enumerate(codes):
        PROXY = proxies[i].get_address()
        for zip in zipcodes:
            webdriver.DesiredCapabilities.CHROME['proxy']={"httpProxy":PROXY,"ftpProxy":PROXY,"sslProxy":PROXY,"proxyType":"MANUAL",}
            webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
            d = webdriver.Chrome(r'C:\Users\Beatrice Tierra\Downloads\chromedriver.exe')
            d.get('https://www.fairhealthconsumer.org/medical/zip')
            location_search = d.find_element_by_css_selector("input[placeholder='Zip Code or City, State (e.g, 12345 or New York, NY)']")
            location_search.send_keys(zip)
            location_search.send_keys(Keys.ENTER)

            time.sleep(3)
            d.find_element_by_xpath("//a[@href='/medical/select-medical-totalcost']").click()

            time.sleep(3)
            cpt_search = d.find_element_by_css_selector("input[placeholder='Enter a CPT Code or Keyword']")
            cpt_search.send_keys('99282')
            cpt_search.send_keys(Keys.ENTER)

            time.sleep(3)
            d.find_element_by_css_selector('[class="button agree"]').click()

            time.sleep(3)
            button = d.find_element_by_css_selector("input[type='radio'][value='99282']")
            d.execute_script("arguments[0].click();", button)

            time.sleep(3)
            d.find_element_by_css_selector('[class="inline-cost-div arrow-btn"]').click()

            time.sleep(3)
            out_net = d.find_element_by_css_selector('[class="circle out-net-summary"]').text
            in_net = d.find_element_by_css_selector('[class="circle in-net-summary"]').text

            writer.writerow([code, zip, in_net, out_net])
            d.close()