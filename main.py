import time

import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

def image_links_scraper(link, max_images):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # initializes driver and installs chromedriver
    driver.get(link) # go to the website 

    image_links = [] # list of links to the images

    current_height = driver.execute_script("return document.body.scrollHeight") # get the starting heigh

    while True: # keep scrolling until we reach the end of the page
        driver.execute_script(f"window.scrollTo({current_height}, document.body.scrollHeight);") # scroll

        elements = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'cover')]") # finds all elements where the 'id' tag starts with the string 'cover'

        if len(elements) >= max_images: # stop scolling if we have scraped enough image links
            break

        time.sleep(5) # wait for page to load

        new_height = driver.execute_script("return document.body.scrollHeight") # get new height after scroll

        if current_height == new_height: # check if the height has stopped changing
            break # if so, we've maxed out and need to stop
        else:
            current_height = new_height # otherwise, we need to keep scrolling

    for element in elements:
        s = element.get_attribute('style') # returns the text in the 'style' attribute
        start = 'width: 100%; min-height: 183px; background-size: cover; background-position: center center; background-repeat: no-repeat; background-image: url("' # first part of the useless substring
        end = '");' # second part of the useless substring
        link = s[len(start):-len(end)] # gets the URL in the string
        image_links.append(link) # add the image link to the list
        print(link)

    return image_links

def download_images(image_links, folder_name):
    i = 1 # keep track of the image number
    for link in image_links: # iterate through all the image links
        r = requests.get(link).content # retrieve the image content from URL
        file_name = f'{folder_name}/{i}.jpg' # generate image file name and directory

        with open(file_name, 'wb') as f:
            f.write(r) # save the image
        
        i += 1 # update the image number for the next iteration

if __name__ == '__main__':
    link = 'https://www.inaturalist.org/taxa/52083-Toxicodendron-pubescens/browse_photos?layout=grid' # website to scrape images
    max_images = 1000
    folder_name = 'images'
    image_links = image_links_scraper(link, max_images)
    download_images(image_links, folder_name)