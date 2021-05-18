import re
import pandas as pd
import csv
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN

class WebScraper:
    def __init__(self, zip, code):
        self.zip = zip
        self.code = code
        self.driver = webdriver.Chrome(r'C:\Users\Beatrice Tierra\Downloads\chromedriver.exe')
        self.driver.get('https://www.fairhealthconsumer.org/medical/zip')

    def enter_location(self):
        location_search = self.driver.find_element_by_css_selector("input[placeholder='Zip Code or City, State (e.g, 12345 or New York, NY)']")
        location_search.send_keys(self.zip)
        location_search.send_keys(Keys.ENTER)

    def submit_location(self):
        time.sleep(20)
        self.driver.find_element_by_xpath("//a[@href='/medical/select-medical-totalcost']").click()

    def enter_cpt(self):
        time.sleep(20) 
        cpt_search = self.driver.find_element_by_css_selector("input[placeholder='Enter a CPT Code or Keyword']")
        cpt_search.send_keys(self.code)
        cpt_search.send_keys(Keys.ENTER)
    
    def agree_to_terms(self): 
        time.sleep(20)
        self.driver.find_element_by_css_selector('[class="button agree"]').click()
    
    def go_to_estimator(self):
        time.sleep(20)
        button = self.driver.find_element_by_css_selector("input[type='radio'][value='{code}']".format(code=self.code))
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(20)
        self.driver.find_element_by_css_selector('[class="inline-cost-div arrow-btn"]').click()

    def get_estimates(self):
        time.sleep(20)
        self.out_net = self.driver.find_element_by_css_selector('[class="circle out-net-summary"]').text
        self.in_net = self.driver.find_element_by_css_selector('[class="circle in-net-summary"]').text

# 1. Get zip codes
csv_file = r'C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Datasets\Addresses.csv'
address_df = pd.read_csv(csv_file)
zipcodes = [re.search('CA \d\d\d\d\d', add).group(0).split(' ')[1] for add in address_df['Address']]

# 2. Initialize VPN
settings = initialize_VPN(save=1,area_input=['complete rotation'])
rotate_VPN(settings)

# 3. Get cost after insurance 
codes = ['99282', '99283', '99284', '99285']
with open('CoverageCost_test2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['CPT Code', 'Zip', 'In-Network', 'Out-Network'])
    for code in codes:
        for i, zip in enumerate(zipcodes): 
            try: 
                # open browser and search zip and cpt code
                browser = WebScraper(zip, code)      
                browser.enter_location() 
                browser.submit_location()   
                browser.enter_cpt()    
                browser.agree_to_terms()   
                browser.go_to_estimator()                               
                browser.get_estimates()       
                in_net, out_net = browser.in_net, browser.out_net             
            except selenium.common.exceptions.ElementNotInteractableException: 
                in_net, out_net = 'N/A', 'N/A'

            # Write to csv
            writer.writerow([code, zip, in_net, out_net])

            # Close driver and check if VPN needs to be switched
            browser.driver.close()   
            if i%5 == 0 and i != 0:
                rotate_VPN(settings)
                time.sleep(10)

terminate_VPN(instructions=None)