import os
import re
import pandas as pd
import csv
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class WebScraper:
    def __init__(self):
        self.driver = webdriver.Chrome(r'C:\Users\Beatrice Tierra\Downloads\chromedriver.exe')
        self.driver.get('https://www.google.com/')

    def enter_location(self):
        location_search = self.driver.find_element_by_name("q")
        location_search.send_keys('Adventist Health Vallejo')
        location_search.send_keys(Keys.RETURN)


web = WebScraper()
web.enter_location()