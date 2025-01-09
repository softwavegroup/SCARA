
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv


options = webdriver.ChromeOptions()
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--disable-features=WebUSB")
driver = webdriver.Chrome(options=options)

url = "https://www.bjs.com/search/juice?pagesize=40&pagenumber=%s"

# how many pages in this shit
num_pages = 1

fname = str(input("FILE NAME: ")) + ".csv"
with open(fname, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
    

        writer.writerow(['Link', 'Name', 'Price', 'UPC', 'Model Number'])

        product_links = {}  # akhane save kor

        for i in range(1, num_pages + 1):
            driver.get(url % i)

            wait = WebDriverWait(driver, 10)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.product-link")))

            product_elements = driver.find_elements(By.CSS_SELECTOR, "a.product-link")

            for product in product_elements:
                link = product.get_attribute("href")
                product_links[link] = None

            time.sleep(random.uniform(5, 10) + (10 * (i % 3)))

            data = ()

            for link in product_links.keys():
                driver.get(link)
                time.sleep(random.uniform(3, 5))
                wait = WebDriverWait(driver, 9)
                product_name = None
                price = None
                upc = None
                model_number = None

                try:
                    name_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.ProductTitle__StyledHeading-sc-r270v3-0.dlSTuQ.mt-0 span[auto-data='product_name']")))
                    product_name = name_element.text
                except Exception as e:
                    product_name = "Name Not Available"

                try:
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.normal-price[auto-data='product_price'] span:nth-child(2)")))
                    price_element = driver.find_element(By.CSS_SELECTOR, "div.normal-price[auto-data='product_price'] span:nth-child(2)")
                    time.sleep(random.uniform(1, 2))
                    price = price_element.text.replace('$', '')  
                except:
                    price = "Member Only"

                try:
                    wait = WebDriverWait(driver, 3)
                    specifications_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@auto-data='product_prodOverview_SpecRadioBtn']")))
                    specifications_tab.click()
                    time.sleep(1)
                    upc_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//th[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'upc')]/following-sibling::td[1]")))
                    upc = upc_element.text.strip()
                except Exception as e:
                    upc = "Not Available"

               

                data += ((link, product_name, price, upc, model_number),)
                
                writer.writerow([link, product_name, price, upc, model_number])
                
    #depend kore crash hoile, wait korish: ak ba dui second is fine
driver.quit()