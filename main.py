import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

link = 'https://www.inaturalist.org/taxa/52083-Toxicodendron-pubescens/browse_photos?layout=grid'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(link)

current_height = driver.execute_script("return document.body.scrollHeight") # get the starting heigh

while True:
    driver.execute_script(f"window.scrollTo({current_height}, document.body.scrollHeight);") # scroll

    time.sleep(10)

    new_height = driver.execute_script("return document.body.scrollHeight") # get new height after scroll

    if current_height == new_height: # check if the height has stopped changing
        break # if so, we've maxed out and need to stop
    else:
        current_height = new_height # otherwise, we need to keep scrolling