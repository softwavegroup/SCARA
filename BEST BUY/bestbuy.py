import requests
import csv 

# Define the base URL for Best Buy's API for categories
api_url = "https://api.bestbuy.com/v1/categories"
# Insert your API key here
api_key = "cVZHAEGg6jOAjjoa8WuGBex9"

# Define the parameters for the request
params = {
    "format": "json",  # Response format
    "pageSize": 100,  # Number of items per page (change as needed)
    "apiKey": api_key,
    "page": 1  # Start from the first page
}

categories = []  # Initialize a list to store categories

# Open a CSV file for writing
with open('best_buy_categories.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['ID', 'Name'])
    
    while True:
        # Make the API request
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extend the categories list with the current batch of categories
            categories.extend(data.get("categories", []))
            # Write each category to the CSV file as it's fetched
            for category in data.get("categories", []):
                writer.writerow([category['id'], category['name']])
            
            # Check if there is a next page
            if params['page'] * params['pageSize'] >= data['total']:
                break  # Exit the loop if we have reached the last page
            params['page'] += 1  # Increment the page number for the next request
        else:
            print(f"Failed to fetch categories, status code: {response.status_code}")
            break

print(f"CSV file has been created with {len(categories)} categories.")