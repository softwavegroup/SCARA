from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time
import undetected_chromedriver as uc
import os
import random
import csv



driver = uc.Chrome()

base_url = "https://www.shoprite.com/sm/planning/rsid/218/categories/international-cuisine/kosher-id-520796?page=2&skip=0"
driver.get(base_url)

num_pages = 999

fname = "jue.csv"
with open(fname, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Price', 'UPC', 'Link'])

    current_page = 1
    while current_page <= num_pages:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid^='ProductCardWrapper']"))
        )

        product_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid^='ProductCardWrapper']")

        for card in product_cards:
            try:
                time.sleep(random.uniform(0.5,.6))
                
                name = card.find_element(By.CSS_SELECTOR, "div.ProductCardNameWrapper--g2y3vm").text
                price = card.find_element(By.CSS_SELECTOR, "div.ProductPrice--w5mr9b").text
                link_element = card.find_element(By.CSS_SELECTOR, "a.ProductCardHiddenLink--f3oc79")
                link = link_element.get_attribute("href")
                upc = card.get_attribute("data-testid").split('-')[-1]

                writer.writerow([name, price, upc, link])
                print([name, price, upc, link])
            except Exception as e:
                print(f"Error processing a product card: {e}")
                time.sleep(random.uniform(0.5, 1))
        
        try:
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='nextPage-button-testId']"))
                )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
            time.sleep(random.uniform(0.5, 2)) 
            next_page_button.click()
        except ElementClickInterceptedException:
            
            print("Click intercepted, attempting JavaScript click.")
            driver.execute_script("arguments[0].click();", next_page_button)

        time.sleep(random.uniform(1, 3))

driver.quit()
