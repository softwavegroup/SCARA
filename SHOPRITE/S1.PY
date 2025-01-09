import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
import time
import random
import csv

def setup_driver():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    return driver

def get_product_details(card):
    try:
        time.sleep(random.uniform(0.5, 0.6))
        name = card.find_element(By.CSS_SELECTOR, "div.ProductCardNameWrapper--g2y3vm").text
        price = card.find_element(By.CSS_SELECTOR, "div.ProductPrice--w5mr9b").text
        link_element = card.find_element(By.CSS_SELECTOR, "a.ProductCardHiddenLink--f3oc79")
        link = link_element.get_attribute("href")
        upc = card.get_attribute("data-testid").split('-')[-1]
        return [name, price, upc, link]
    except NoSuchElementException as e:
        print(f"Error processing a product card: {e}")
        return None

def main():
    base_url = "https://www.shoprite.com/sm/planning/rsid/218/categories/international-cuisine/kosher-id-520796?page=2&skip=0"
    num_pages = 14
    fname = "SpfJewishFoood.csv"

    driver = setup_driver()
    driver.get(base_url)

    with open(fname, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Price', 'UPC', 'Link'])

        current_page = 1
        while current_page <= num_pages:
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid^='ProductCardWrapper']"))
                )
                product_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid^='ProductCardWrapper']")

                for card in product_cards:
                    product_details = get_product_details(card)
                    if product_details:
                        writer.writerow(product_details)
                        print(product_details)

                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='nextPage-button-testId']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
                time.sleep(random.uniform(0.5, 2))
                next_page_button.click()

                current_page += 1
                time.sleep(random.uniform(1, 3))

            except (TimeoutException, ElementClickInterceptedException) as e:
                print(f"Error navigating to the next page: {e}")
                driver.execute_script("arguments[0].click();", next_page_button)
                time.sleep(random.uniform(1, 3))
                current_page += 1

    driver.quit()

if __name__ == "__main__":
    main()
