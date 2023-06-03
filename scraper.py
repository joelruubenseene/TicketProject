# Author: Joel Ruuben Seene
# Project idea: scraper for https://elron.pilet.ee/et/otsing/<start>/<destination>/<date: YYYY-MM-DD>

import requests
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

driver_exe = 'chromedriver'
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(driver_exe, options=options)

headers = {
    # User-Agent header to bypass spider/scraper protection, just in case
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
}

start = input("Input starting stop: ")
destination = input("Input destination: ")
date = input("Input date (leave empty for today): ")

if date == '':  # If the input is empty, add current date (YYYY-MM-DD)
    date = str(datetime.date.today())


url = 'https://elron.pilet.ee/et/otsing/' + start + '/' + destination + '/' + date + '/' # Construct the url

response = requests.get(url).status_code
if response == 200:
    print("URL accessible")
    driver.get(url)
else:
    print(f"Bad URL, status: " + response)


