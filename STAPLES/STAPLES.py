from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
# options.headless = True  # Uncomment to run Chrome in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')
# Replace this URL with the actual page you want to scrape
url = 'https://www.walmart.com/'
driver.get(url)

# Wait for the dynamic content to load
time.sleep(35)  # Adjust time as necessary
wait = WebDriverWait(driver, 10)
# Find all product divs
products = driver.find_elements(By.CSS_SELECTOR, 'div.mb0.ph1.ph0-xl.pt0-xl.pb3-m.bb.b--near-white.w-25')

for product in products:
    # Extract the title and href from each product
    title_element = product.find_element(By.CSS_SELECTOR, 'a > span')
    title = title_element.text if title_element else 'No Title Found'
    
    href_element = product.find_element(By.CSS_SELECTOR, 'a')
    href = href_element.get_attribute('href') if href_element else 'No Link Found'
    
    print(f'Title: {title}\nLink: {href}\n')

# Don't forget to quit the driver
driver.quit()
