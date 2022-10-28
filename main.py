import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

def image_links_scraper(link):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # initializes driver and installs chromedriver
    driver.get(link) # go to the website 

    image_links = [] # list of links to the images

    current_height = driver.execute_script("return document.body.scrollHeight") # get the starting heigh

    while True: # keep scrolling until we reach the end of the page
        driver.execute_script(f"window.scrollTo({current_height}, document.body.scrollHeight);") # scroll

        time.sleep(5) # wait for page to load

        new_height = driver.execute_script("return document.body.scrollHeight") # get new height after scroll

        if current_height == new_height: # check if the height has stopped changing
            break # if so, we've maxed out and need to stop
        else:
            break
            #current_height = new_height # otherwise, we need to keep scrolling

    elements = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'cover')]")
    for element in elements:
        link = element.get_attribute('style')
        image_links.append(link)
        print(link)
    
    return image_links

if __name__ == '__main__':
    link = 'https://www.inaturalist.org/taxa/52083-Toxicodendron-pubescens/browse_photos?layout=grid' # website to scrape images
    image_links_scraper(link)