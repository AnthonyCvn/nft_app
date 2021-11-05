import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import scraping_function as sf

import time


# Configure selenium and web driver
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path='./chromedriver')

def get_dataframe_raritytool():
    
    # Get the data from https://rarity.tools/upcoming and return a Panda DataFrame with the information about all upcoming nfts that we find.
    
    
    driver.get('https://rarity.tools/upcoming')

    time.sleep(3) # TODO: implement a more systematic way

    url_elements = driver.find_elements_by_xpath("//*[contains(@class,'text-left text-gray-800')]")

    nft_list = []
    for element in url_elements:
        nft_list.append(element.text.split('\n'))

    df = pd.DataFrame(nft_list)

    nft_df = df.drop(labels=[2, 5, 6, 7, 8, 9, 10, 11, 12, 13], axis=1)
    nft_df.columns = ['Name', 'Description', 'Twitter', 'Website']

    return nft_df


