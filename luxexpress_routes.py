from time import sleep
import json

from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://luxexpress.eu/en/all-routes/"

# Make the browser operate in headless mode to avoid pop-up
options = webdriver.FirefoxOptions()
options.add_argument("--headless")

# Make the queries
browser = webdriver.Firefox(options=options)
browser.get(url)

sleep(2)  # Quick 'n' dirty way to wait for the JS to load the data
html_content = browser.page_source

soup = BeautifulSoup(html_content, 'html.parser')

try:
    class_name = "AllRoutes_direction__hnW3q"
    elements_with_class = soup.find_all('a', class_=class_name)

    link_dict = {}
    for element in elements_with_class:
        # Find the departure and arrival stop names to create the key for dict (route_name)
        departure = element.find("div", class_="AllRoutes_departure__Jtfjx").text
        arrival = element.find("div", class_="AllRoutes_arrival__CSehE").text
        route_name = departure + "-" + arrival

        # Find the link to the route search page
        href = element.get('href')
        href = "https://luxexpress.eu" + href
        link_dict[route_name] = href  # Add to the dictionary

    filename = "luxexpress_routes" + ".json"  # Filename to save the result to

    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(link_dict, json_file, indent=4, ensure_ascii=False)
    print(f"JSON response saved to {filename}")  # Notify of successful operation

except AttributeError or KeyboardInterrupt:
    print("[ERROR] - Cannot find links to scrape")

browser.close()
