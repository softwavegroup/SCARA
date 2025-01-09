import requests
from bs4 import BeautifulSoup

def scrape_costco_products(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_tiles = soup.find_all('div', class_='product-tile-set')
        
        for tile in product_tiles:
            product_info = tile.find('div', class_='caption')
            product_name = product_info.find('span', class_='description').text.strip()
            product_price = product_info.find('div', class_='price').text.strip()
            product_url = tile['data-pdp-url']
            
            print(f'Product Name: {product_name}, Price: {product_price}, URL: {product_url}')
    else:
        print("Failed to retrieve data")

# Example usage
url = 'https://www.costco.com/household.html'
scrape_costco_products(url)
