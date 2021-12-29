from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os

s = Service("/usr/local/bin/chromedriver")

# automates download of UBVRI file
def isochrone_file():
    driver = webdriver.Chrome(service=s)
    driver.get("http://waps.cfa.harvard.edu/MIST/model_grids.html")
    driver.maximize_window()
    driver.find_element_by_link_text("UBV(RI)c + 2MASS + Kepler + Hipparcos + Tycho + Gaia (114MB)").click()

isochrone_file()
