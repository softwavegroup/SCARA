from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import csv
import json

try:
    driver = uc.Chrome()
    driver.get("https://www.walmart.com/search?q=trash+bags")
    WebDriverWait(driver, 21).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-item-id]")))
    actions = ActionChains(driver)

    with open('walmarttestupc.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name', 'URL', 'Price', 'UPC'])

        product_links = []
        while True:
            product_containers = driver.find_elements(By.CSS_SELECTOR, "div[data-item-id]")
            for container in product_containers:
                actions.move_to_element(container).perform()
                time.sleep(2)
                name = container.find_element(By.CSS_SELECTOR, "span[data-automation-id='product-title']").text
                link = container.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                product_links.append((name, link))
                try:
                    price_element = WebDriverWait(container, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-automation-id='product-price'] div"))
                    )
                    price = price_element.text
                except:
                    price = "Not available"
                writer.writerow([name, link, price, ''])  # Placeholder for UPC
                print(f"Product: {name}, URL: {link}, Price: {price}")
                time.sleep(2)

            next_page_button = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='NextPage']")
            if not next_page_button or 'b--light-gray' in next_page_button[0].get_attribute('class'):
                break
            next_page_button[0].click()
            WebDriverWait(driver, 21).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-item-id]")))
            time.sleep(3)

        # Additional loop to visit each product page and get the UPC
        for name, link in product_links:
            driver.get(link)
            time.sleep(5)  # Slow down to avoid overwhelming the website
            page_source = driver.page_source
            start = page_source.find('<script type="application/ld+json">')
            if start != -1:
                end = page_source.find('</script>', start)
                json_text = page_source[start + len('<script type="application/ld+json">'):end]
                try:
                    data = json.loads(json_text)
                    upc = data.get('gtin13', 'Not available')
                except json.JSONDecodeError:
                    upc = 'Not available'
                writer.writerow([name, link, '', upc])  # Append UPC to existing row
                print(f"Product: {name}, UPC: {upc}")
            time.sleep(5)

except KeyboardInterrupt:
    print("Interrupted by user, closing the driver.")
finally:
    driver.quit()
