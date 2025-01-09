import requests
import csv

def fetch_headphone_products(filename):
    url = 'https://api.bestbuy.com/v1/products((search=mp3)&freeShipping=true&inStoreAvailability=true)?apiKey=cVZHAEGg6jOAjjoa8WuGBex9&sort=upc.asc&show=upc,regularPrice,salePrice,categoryPath.name,image&format=json'    
    params = {
    
        "format": "json",
        "pageSize": 100,  # Adjust as necessary
        "page": 1
    }
    products = []
    
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            products.extend(data.get("products", []))
            if params['page'] * params['pageSize'] >= data['total']:
                break
            params['page'] += 1
        else:
            print(f"Failed to fetch products, status code: {response.status_code}")
            break
    
    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'UPC', 'Regular Price', 'Sale Price', 'Online Availability', 'Image Link'])
        for product in products:
            writer.writerow([
                product.get('name', ''),
                product.get('upc', ''),
                product.get('regularPrice', ''),
                product.get('salePrice', ''),
                "Yes" if product.get('onlineAvailability', False) else "No",
                product.get('image', '')
            ])
    
    print(f"CSV file has been created with {len(products)} products.")
    
filename = input("file name: ")

fetch_headphone_products(filename)
