import requests
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class WebScraper:
    def __init__(self, hospital):
        self.hospital = hospital
        self.driver = webdriver.Chrome(r'C:\Users\Beatrice Tierra\Downloads\chromedriver.exe')
        self.driver.get('https://www.google.com/')        
    
    def sleep(self):
        time.sleep(3)

    def enter_hospital(self):
        hospital_search = self.driver.find_element_by_name("q")
        hospital_search.send_keys('{hospital} insurance'.format(hospital=self.hospital))
        hospital_search.send_keys(Keys.RETURN)

    def click_website(self):
        self.sleep()
        website = self.driver.find_element_by_tag_name('h3')
        website.click()
    
    def read_page(self):
        self.url = self.driver.current_url
        html = requests.get(self.driver.current_url)
        soup = BeautifulSoup(html.text, features='lxml')
        self.sleep()
        text = soup.get_text(strip=True)
        self.sleep()
        return text

# 1. Get name of hopsitals
hospital_xlsx = r"Datasets/CAHospitals.xlsx"
hospital_df = pd.read_excel(hospital_xlsx)
hospitals = hospital_df['Hospital Name'].values

# 2. Get list of insurance
insurance_xlsx = r"Datasets/CAInsurances.xlsx"
insurance_df = pd.read_excel(insurance_xlsx)
insurances = insurance_df['Common Alias'].values

# 3. Check if insurance listed on page
with open('AcceptedInsurance.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Hospital', 'Accepted Insurances', 'Website'])
    for hospital in hospitals:
        try:
            browser = WebScraper(hospital)
            browser.enter_hospital()
            browser.click_website()
            text = browser.read_page()

            accepted_insurances = []
            for insurance in insurances:
                if insurance.lower() in text.lower():
                    accepted_insurances.append(insurance)
            
        except:
            accepted_insurances = 'N/A'

        writer.writerow([hospital, accepted_insurances, browser.url])
        browser.driver.close()   