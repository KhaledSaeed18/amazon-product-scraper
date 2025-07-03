"""
Amazon Product Scraper

This script scrapes basic product information (title and price) from Amazon product pages
using Beautiful Soup and requests. It mimics a browser request to avoid being blocked.
"""

import requests
from bs4 import BeautifulSoup

# HTTP headers to mimic a real browser request and avoid getting blocked by Amazon
headers = {
    # User-Agent string identifies the browser type and version
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    # Accept-Language specifies preferred language for the response
    'Accept-Language': 'en-US,en;q=0.5'
}


def get_product_details(product_url: str) -> dict:
    """
    Scrapes product details from an Amazon product page.
    
    Args:
        product_url (str): The URL of the Amazon product page to scrape
        
    Returns:
        dict: A dictionary containing 'title' and 'price' keys with scraped values, or None if scraping fails
    """
    # Create an empty product details dictionary
    product_details = {}

    # Send HTTP GET request to the product URL with browser-like headers
    page = requests.get(product_url, headers=headers)
    
    # Parse the HTML content using Beautiful Soup with lxml parser for better performance
    soup = BeautifulSoup(page.content, features="lxml")
    
    try:
        # Scrape the product title using the specific span element with 'productTitle' ID
        title = soup.find(
            'span', attrs={'id': 'productTitle'}).get_text().strip()
        
        # Scrape the price from the span element with 'a-price' class
        extracted_price = soup.find(
            'span', attrs={'class': 'a-price'}).get_text().strip()
        
        # Clean up the price string by extracting only the part after the first '$' symbol
        price = '$' + extracted_price.split('$')[1]

        # Store the scraped data in the product details dictionary
        product_details['title'] = title
        product_details['price'] = price

        # Return the populated product details dictionary
        return product_details
        
    except Exception as e:
        # Handle any errors that occur during scraping (missing elements, network issues, etc.)
        print('Could not fetch product details')
        print(f'Failed with exception: {e}')
        return None


# Main execution section
if __name__ == "__main__":
    # Get the Amazon product URL from user input
    product_url = input('Enter product url: ')
    
    # Call the scraping function to get product details
    product_details = get_product_details(product_url)

    # Display the scraped product information
    print(product_details)