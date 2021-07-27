import os
import re
import pandas as pd
import csv
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN

chrome_options = Options()
chrome_options.add_argument("--headless")

class WebScraper:
    def __init__(self, zip, code):
        self.zip = zip
        self.code = code
        self.driver = webdriver.Chrome(r'C:\Users\Beatrice Tierra\Downloads\chromedriver.exe',
                                        options=chrome_options)
        self.driver.get('https://www.fairhealthconsumer.org/medical/zip')

    def sleep(self):
        time.sleep(5)

    def enter_location(self):
        location_search = self.driver.find_element_by_css_selector("input[placeholder='Zip Code or City, State (e.g, 12345 or New York, NY)']")
        location_search.send_keys(self.zip)
        location_search.send_keys(Keys.ENTER)

    def submit_location(self):
        self.sleep()
        self.driver.find_element_by_xpath("//a[@href='/medical/select-medical-totalcost']").click()

    def enter_cpt(self):
        self.sleep()
        cpt_search = self.driver.find_element_by_css_selector("input[placeholder='Enter a CPT Code or Keyword']")
        cpt_search.send_keys(self.code)
        cpt_search.send_keys(Keys.ENTER)
    
    def agree_to_terms(self): 
        self.sleep()
        self.driver.find_element_by_css_selector('[class="button agree"]').click()
    
    def go_to_estimator(self):
        self.sleep()
        button = self.driver.find_element_by_css_selector("input[type='radio'][value='{code}']".format(code=self.code))
        self.driver.execute_script("arguments[0].click();", button)
        self.sleep()
        self.driver.find_element_by_css_selector('[class="inline-cost-div arrow-btn"]').click()

    def get_estimates(self):
        self.sleep()
        self.out_net = self.driver.find_element_by_css_selector('[class="circle out-net-summary"]').text
        self.in_net = self.driver.find_element_by_css_selector('[class="circle in-net-summary"]').text

# Check if data already stored in csv file
def check_row(reader, zip, code):
    row_exists = any((row[0] == code) and (row[1] == zip) for row in reader)
    return row_exists

# open browser and search zip and cpt code
def run_browser(zip, code):
    browser = WebScraper(zip, code)      
    browser.enter_location() 
    browser.submit_location()   
    browser.enter_cpt()    
    browser.agree_to_terms()   
    browser.go_to_estimator()                               
    browser.get_estimates()       
    in_net, out_net = browser.in_net, browser.out_net  
    return browser, in_net, out_net

# 1. Get zip codes
csv_file = r'C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Datasets\Addresses.csv'
address_df = pd.read_csv(csv_file)
zipcodes = [re.search('CA \d\d\d\d\d', add).group(0).split(' ')[1] for add in address_df['Address']]

# 2. Initialize VPN
settings = initialize_VPN(save=1,area_input=['complete rotation'])
rotate_VPN(settings)

# 3. Create csv file to store data
filename = 'Datasets/CoverageCost.csv'
if not os.path.exists(filename):
    open(filename, 'w').close()

# 4. Get cost after insurance 
csv_headers = ['CPT Code', 'Zip', 'In-Network', 'Out-Network']
codes = ['99282', '99283', '99284', '99285']

with open(filename, "r") as rf, open(filename, "a", newline='') as wf:
    reader = csv.reader(rf)
    writer = csv.writer(wf)
    if not check_row(reader, 'Zip', 'CPT Code'):
        writer.writerow(csv_headers)
    for code in codes:
        for i, zip in enumerate(zipcodes):
            if not check_row(reader, zip, code):
                try: 
                    # open browser and search zip and cpt code
                    browser, in_net, out_net = run_browser(zip, code)
                    print(in_net, out_net)           
                except selenium.common.exceptions.ElementNotInteractableException: 
                    in_net, out_net = 'N/A', 'N/A'
                except selenium.common.exceptions.WebDriverException:
                    browser.driver.close() 
                    rotate_VPN(settings)
                    time.sleep(2)
                    browser, in_net, out_net = run_browser(zip, code)
                    print(in_net, out_net)  

                # Write to csv
                writer.writerow([code, zip, in_net, out_net])

                # Close driver and check if VPN needs to be switched
                browser.driver.close()   
                if i%5 == 0 and i != 0:
                    rotate_VPN(settings)
                    time.sleep(2)

terminate_VPN(instructions=None)