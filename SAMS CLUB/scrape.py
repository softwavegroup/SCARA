import requests
from bs4 import BeautifulSoup
import csv
import re

def scrape_website(base_url, pages):
    offset = 0
    # Open a CSV file to store the data
    with open('seasoning.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Product Title', 'Current Price', 'Picture Link'])

        for page in range(pages):
            # Construct the URL with the current offset
            url = f"{base_url}?offset={offset}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', class_='sc-pc-medium-desktop-card-canary')

            for product in products:
                # Extract product title
                title = product.find('div', class_='sc-pc-title-medium').text.strip()
                # Extract product price
                price_info = product.find('div', class_='sc-pc-single-price').text.strip()
                # Use regex to find the first price
                current_price_match = re.search(r'current price: (\$\d+\.\d{2})', price_info)
                current_price = current_price_match.group(1) if current_price_match else None
                # Extract picture link
                picture_link = product.find('img')['src']

                # Write the product data to the CSV file
                writer.writerow([title, current_price, picture_link])

            # Increment the offset for the next page
            offset += 45
            print(f'yo gang scraped page {page + 1}')

    print('Data scraped and saved to products.csv')

# Example usage
base_url = 'https://www.samsclub.com/b/spices-seasonings/1544'
pages_to_scrape = 3 # Set the number of pages you want to scrape
scrape_website(base_url, pages_to_scrape)

