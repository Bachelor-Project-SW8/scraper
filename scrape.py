import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = 'https://www.trendhim.com/armband/c7'

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Check for request errors

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all product containers (anchor tags that contain the product info)
products = soup.find_all('a', class_='ProductTilesV2_ProductTileV2__IlocW')

# Initialize lists to store product details
product_names = []
product_prices = []
product_images = []
product_brands = []

# Loop through each product and extract details
for product in products:
    # Extract product name (from <p class="ProductTilesV2_title___1WBp">)
    name_tag = product.find('p', class_='ProductTilesV2_title___1WBp')
    name = name_tag.get_text(strip=True) if name_tag else 'N/A'
    product_names.append(name)

    # Extract product price (from <div class="ProductTilesV2_price__4KH_9">)
    price_tag = product.find('div', class_='ProductTilesV2_price__4KH_9')
    if price_tag:
        # Try to find the actual price (second <p> element)
        price = price_tag.find_all('p')[1].get_text(strip=True) if len(price_tag.find_all('p')) > 1 else 'N/A'
    else:
        price = 'N/A'
    product_prices.append(price)

    # Extract product image URL (from <img class="ProductTilesV2_image__1aUm4">)
    image_tag = product.find('img', class_='ProductTilesV2_image__1aUm4')
    image_url = image_tag['src'] if image_tag else 'N/A'
    product_images.append(image_url)

    # Extract product brand (from <p class="ProductTilesV2_brand__64Pqm">)
    brand_tag = product.find('p', class_='ProductTilesV2_brand__64Pqm')
    brand = brand_tag.get_text(strip=True) if brand_tag else 'N/A'
    product_brands.append(brand)

# Create a DataFrame to store the data
df = pd.DataFrame({
    'Product Name': product_names,
    'Price': product_prices,
    'Image URL': product_images,
    'Brand': product_brands
})

# Export the data to a CSV file
df.to_csv('trendhim_bracelets.csv', index=False, encoding='utf-8')

print('Data has been successfully scraped and saved to trendhim_bracelets.csv')
