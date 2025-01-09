import time
import random
import csv
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

def main():
    # --- Selenium driver and options ---
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-features=WebUSB')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    )

    driver = webdriver.Chrome(options=options)

    # --- Target URL pattern ---
    base_url = "https://www.bjs.com/search/chips/q?template=clp&pagenumber={}"

    # --- Number of pages to scrape ---
    num_pages = 4

    # --- File name prompt ---
    fname = input("FILE NAME: ").strip() + ".csv"

    # --- Open CSV for writing ---
    with open(fname, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Link', 'Name', 'Price', 'UPC', 'Stock Status'])

        product_links = set()  # using a set to avoid duplicates

        for page_number in range(1, num_pages + 1):
            # --- Navigate to search results page ---
            page_url = base_url.format(page_number)
            driver.get(page_url)

            # --- Attempt to handle store-locator or membership popups, if any ---
            # Depending on the site’s behavior, you might need to detect and close them:
            # try:
            #     # Example popup close button
            #     popup_close = WebDriverWait(driver, 5).until(
            #         EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close-button"))
            #     )
            #     popup_close.click()
            #     time.sleep(1)
            # except TimeoutException:
            #     pass

            # --- Wait for product grid or product links to appear ---
            try:
                wait = WebDriverWait(driver, 20)
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.product-link"))
                )
                product_elements = driver.find_elements(By.CSS_SELECTOR, "a.product-link")

                # Collect unique product links
                for product in product_elements:
                    href = product.get_attribute("href")
                    if href:
                        product_links.add(href)

            except TimeoutException:
                print(f"[WARNING] Timed out waiting for product links on page {page_number}.", file=sys.stderr)
                # Optionally continue to the next page instead of halting
                continue

            # --- Random sleep to mimic human browsing ---
            time.sleep(random.uniform(5, 10) + (10 * (page_number % 3)))

        # --- Now iterate over each product link we found ---
        for link in product_links:
            driver.get(link)
            time.sleep(random.uniform(2, 4))

            # Scroll a bit to ensure elements load (sometimes required)
            driver.execute_script("window.scrollBy(0, 400);")

            # Use a short wait for product details
            wait = WebDriverWait(driver, 10)

            # Default placeholders
            product_name = "Name Not Available"
            price = "Member Only"
            upc = "Not Available"
            stock_status = "Status not found"

            # --- Extract product name ---
            try:
                # Wait for the heading that contains the product name
                name_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                        "h1.ProductTitle__StyledHeading-sc-r270v3-0 span[auto-data='product_name']"))
                )
                product_name = name_element.text.strip()
            except TimeoutException:
                pass

            # --- Extract price ---
            try:
                # Price may load as a normal price or a member price
                wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.normal-price[auto-data='product_price'] span:nth-child(2)")
                    )
                )
                price_element = driver.find_element(By.CSS_SELECTOR,
                    "div.normal-price[auto-data='product_price'] span:nth-child(2)")
                price = price_element.text.replace('$', '').strip()
            except (TimeoutException, Exception):
                pass

            # --- Extract UPC from the specifications tab ---
            try:
                spec_tab_wait = WebDriverWait(driver, 5)
                specifications_tab = spec_tab_wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@auto-data='product_prodOverview_SpecRadioBtn']"))
                )
                specifications_tab.click()
                time.sleep(1)
                upc_element = spec_tab_wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//th[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'upc')]/following-sibling::td[1]"
                        )
                    )
                )
                upc = upc_element.text.strip()
            except TimeoutException:
                pass

            # --- Extract stock status ---
            try:
                stock_wait = WebDriverWait(driver, 5)
                stock_status_element = stock_wait.until(
                    EC.visibility_of_element_located((
                        By.XPATH,
                        "(//div[contains(@class, 'inventory-available') or contains(@class, 'inventory-na')]//span)[1]"
                    ))
                )
                stock_status = stock_status_element.text.strip()
            except TimeoutException:
                pass

            # --- Write row to CSV ---
            writer.writerow([link, product_name, price, upc, stock_status])
            # Print to console if desired
            # print(link, product_name, price, upc, stock_status)

    driver.quit()

if __name__ == "__main__":
    main()
