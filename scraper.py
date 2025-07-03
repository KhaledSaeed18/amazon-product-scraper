"""
Amazon Product Scraper

This script scrapes basic product information (title and price) from Amazon product pages
using Beautiful Soup and requests. It mimics a browser request to avoid being blocked.
"""

import requests
from bs4 import BeautifulSoup
import time
import threading
import sys

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


def spinner_animation(stop_event):
    """
    Display a spinning animation while loading.
    
    Args:
        stop_event: Threading event to stop the spinner
    """
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\r{spinner_chars[i]} Fetching product details...')
        sys.stdout.flush()
        i = (i + 1) % len(spinner_chars)
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 50 + '\r')  # Clear the line
    sys.stdout.flush()


def get_product_details_with_loading(product_url: str) -> dict:
    """
    Wrapper function to scrape product details with loading animation.
    
    Args:
        product_url (str): The URL of the Amazon product page to scrape
        
    Returns:
        dict: A dictionary containing 'title' and 'price' keys with scraped values, or None if scraping fails
    """
    # Create a stop event for the spinner
    stop_event = threading.Event()
    
    # Start the spinner in a separate thread
    spinner_thread = threading.Thread(target=spinner_animation, args=(stop_event,))
    spinner_thread.start()
    
    try:
        # Call the original scraping function
        result = get_product_details(product_url)
        return result
    finally:
        # Stop the spinner
        stop_event.set()
        spinner_thread.join()


# Main execution section
if __name__ == "__main__":
    print("🛒 Amazon Product Scraper")
    print("=" * 30)
    
    # Get the Amazon product URL from user input
    product_url = input('Enter product url: ')
    
    print()  # Add some spacing
    
    # Call the scraping function with loading animation
    product_details = get_product_details_with_loading(product_url)

    # Display the scraped product information with nice formatting
    if product_details:
        print("✅ Product details fetched successfully!")
        print("=" * 40)
        print(f"📝 Title: {product_details['title']}")
        print(f"💰 Price: {product_details['price']}")
        print("=" * 40)
    else:
        print("❌ Failed to fetch product details. Please check the URL and try again.")