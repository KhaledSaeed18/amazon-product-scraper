"""
Amazon Product Scraper

This script scrapes basic product information from Amazon product pages
using Beautiful Soup and requests. It mimics a browser request to avoid being blocked.
"""

import requests
from bs4 import BeautifulSoup
import time
import threading
import sys
import re
import json
from datetime import datetime
from urllib.parse import urlparse

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

        # Scrape the rating from the span element within the star icon
        rating_element = soup.find('i', attrs={'class': lambda x: x and 'a-icon-star' in x})
        rating = None
        if rating_element:
            rating_span = rating_element.find('span', attrs={'class': 'a-icon-alt'})
            if rating_span:
                rating_text = rating_span.get_text().strip()
                # Extract the numeric rating (e.g., "4.4" from "4.4 out of 5 stars")
                rating = rating_text.split(' ')[0]

        # Scrape the number of ratings
        num_ratings = None
        ratings_element = soup.find('span', attrs={'id': 'acrCustomerReviewText'})
        if ratings_element:
            ratings_text = ratings_element.get_text().strip()
            # Extract the number from text like "576 ratings" or "576 Reviews"
            num_ratings = ratings_text.split(' ')[0]

        # Scrape the main product image
        image_url = None
        image_element = soup.find('img', attrs={'id': 'landingImage'})
        if image_element:
            # Try to get the high-resolution image from data-old-hires attribute first
            image_url = image_element.get('data-old-hires')
            # If not available, fall back to the src attribute
            if not image_url:
                image_url = image_element.get('src')

        # Scrape the "About this item" bullet points
        about_item = []
        feature_bullets = soup.find('div', attrs={'id': 'feature-bullets'})
        if feature_bullets:
            bullet_list = feature_bullets.find('ul', attrs={'class': 'a-unordered-list'})
            if bullet_list:
                bullets = bullet_list.find_all('li')
                for bullet in bullets:
                    span = bullet.find('span', attrs={'class': 'a-list-item'})
                    if span:
                        bullet_text = span.get_text().strip()
                        if bullet_text:  # Only add non-empty bullet points
                            about_item.append(bullet_text)

        # Scrape the breadcrumb navigation for product categorization
        breadcrumbs = []
        breadcrumb_div = soup.find('div', attrs={'id': 'wayfinding-breadcrumbs_feature_div'})
        if breadcrumb_div:
            breadcrumb_list = breadcrumb_div.find('ul', attrs={'class': 'a-unordered-list'})
            if breadcrumb_list:
                # Find all list items that contain links (categories)
                breadcrumb_items = breadcrumb_list.find_all('li')
                for item in breadcrumb_items:
                    # Skip divider elements
                    if 'a-breadcrumb-divider' not in item.get('class', []):
                        link = item.find('a', attrs={'class': 'a-link-normal'})
                        if link:
                            category_text = link.get_text().strip()
                            if category_text:
                                breadcrumbs.append(category_text)

        # Store the scraped data in the product details dictionary
        product_details['title'] = title
        product_details['price'] = price
        product_details['rating'] = rating
        product_details['num_ratings'] = num_ratings
        product_details['image_url'] = image_url
        product_details['about_item'] = about_item
        product_details['breadcrumbs'] = breadcrumbs

        # Return the populated product details dictionary
        return product_details
        
    except Exception as e:
        # Handle any errors that occur during scraping (missing elements, network issues, etc.)
        print('Could not fetch product details')
        print(f'Failed with exception: {e}')
        return None


def spinner_animation(stop_event, message="Fetching product details..."):
    """
    Display a spinning animation while loading.
    
    Args:
        stop_event: Threading event to stop the spinner
        message: Custom loading message to display
    """
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\r{spinner_chars[i]} {message}')
        sys.stdout.flush()
        i = (i + 1) % len(spinner_chars)
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')  # Clear the line
    sys.stdout.flush()


def get_product_details_with_loading(product_url: str, product_index: int = None, total_products: int = None) -> dict:
    """
    Wrapper function to scrape product details with loading animation.
    
    Args:
        product_url (str): The URL of the Amazon product page to scrape
        product_index (int): Current product index (for multiple products)
        total_products (int): Total number of products (for multiple products)
        
    Returns:
        dict: A dictionary containing 'title' and 'price' keys with scraped values, or None if scraping fails
    """
    # Create a stop event for the spinner
    stop_event = threading.Event()
    
    # Customize loading message based on whether we're processing multiple products
    if product_index is not None and total_products is not None:
        loading_message = f"Fetching product {product_index}/{total_products}..."
    else:
        loading_message = "Fetching product details..."
    
    # Start the spinner in a separate thread
    spinner_thread = threading.Thread(target=spinner_animation, args=(stop_event, loading_message))
    spinner_thread.start()
    
    try:
        # Call the original scraping function
        result = get_product_details(product_url)
        return result
    finally:
        # Stop the spinner
        stop_event.set()
        spinner_thread.join()


def validate_amazon_url(url: str) -> bool:
    """
    Validates if the provided URL is a valid Amazon product URL.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        bool: True if valid Amazon product URL, False otherwise
    """
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        
        # Check if the scheme is http or https
        if parsed_url.scheme not in ['http', 'https']:
            return False
        
        # Check if the domain is Amazon
        domain = parsed_url.netloc.lower()
        amazon_domains = [
            'amazon.com', 'www.amazon.com',
            'amazon.co.uk', 'www.amazon.co.uk',
            'amazon.ca', 'www.amazon.ca',
            'amazon.de', 'www.amazon.de',
            'amazon.fr', 'www.amazon.fr',
            'amazon.it', 'www.amazon.it',
            'amazon.es', 'www.amazon.es',
            'amazon.in', 'www.amazon.in',
            'amazon.co.jp', 'www.amazon.co.jp',
            'amazon.com.au', 'www.amazon.com.au'
        ]
        
        if domain not in amazon_domains:
            return False
        
        # Check if the URL contains product identifiers
        path = parsed_url.path.lower()
        
        # Amazon product URLs typically contain '/dp/' or '/gp/product/' patterns
        product_patterns = [
            r'/dp/[a-z0-9]{10}',  # Standard product page pattern
            r'/gp/product/[a-z0-9]{10}',  # Alternative product page pattern
            r'/[^/]+/dp/[a-z0-9]{10}',  # Category + product pattern
        ]
        
        for pattern in product_patterns:
            if re.search(pattern, path):
                return True
        
        return False
        
    except Exception:
        return False


def get_multiple_urls() -> list:
    """
    Get multiple product URLs from user input.
    
    Returns:
        list: List of validated Amazon product URLs
    """
    urls = []
    print("📝 Enter Amazon product URLs (press Enter twice when done):")
    print("   💡 Tip: You can paste one URL per line")
    print()
    
    url_count = 1
    while True:
        url = input(f"URL {url_count}: ").strip()
        
        if not url:  # Empty input
            if urls:  # If we have at least one URL, break
                break
            else:  # If no URLs entered yet, continue asking
                print("   ⚠️  Please enter at least one URL.")
                continue
        
        if validate_amazon_url(url):
            urls.append(url)
            print(f"   ✅ URL {url_count} added successfully!")
            url_count += 1
        else:
            print("   ❌ Invalid Amazon URL. Please try again.")
    
    return urls


def display_configuration_menu() -> int:
    """
    Display configuration menu and get user's choice.
    
    Returns:
        int: User's choice (1 for single URL, 2 for multiple URLs)
    """
    print("🛒 Amazon Product Scraper - Configuration")
    print("=" * 45)
    print()
    print("📋 Choose scraping mode:")
    print("   1️⃣  Single Product URL")
    print("   2️⃣  Multiple Product URLs")
    print()
    
    while True:
        try:
            choice = input("Select option (1 or 2): ")

            if choice in ['1', '2']:
                return int(choice)
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("❌ Invalid input. Please enter 1 or 2.")


def display_single_product(product_details: dict, url: str) -> None:
    """
    Display details for a single product.
    
    Args:
        product_details (dict): Product details dictionary
        url (str): Product URL
    """
    if product_details:
        print("✅ Product details fetched successfully!")
        print("=" * 40)
        print(f"📝 Title: {product_details['title']}")
        print(f"💰 Price: {product_details['price']}")
        
        # Display breadcrumb categories
        if product_details['breadcrumbs']:
            breadcrumb_path = " › ".join(product_details['breadcrumbs'])
            print(f"📂 Category: {breadcrumb_path}")
        else:
            print("📂 Category: Not available")
        
        # Display rating
        if product_details['rating']:
            rating_display = f"⭐ Rating: {product_details['rating']}/5"
            if product_details['num_ratings']:
                rating_display += f" ({product_details['num_ratings']} ratings)"
            print(rating_display)
        else:
            print("⭐ Rating: Not available")
            
        # Display image URL
        if product_details['image_url']:
            print(f"🖼️  Image: {product_details['image_url']}")
        else:
            print("🖼️  Image: Not available")
            
        # Display product URL
        print(f"🔗 URL: {url}")
            
        # Display "About this item" bullet points
        if product_details['about_item']:
            print(f"📋 About this item:")
            for i, bullet in enumerate(product_details['about_item'], 1):
                # Wrap long text for better readability (max 80 characters per line)
                wrapped_text = []
                words = bullet.split(' ')
                current_line = f"   {i}. "
                
                for word in words:
                    if len(current_line + word) <= 80:
                        current_line += word + " "
                    else:
                        wrapped_text.append(current_line.rstrip())
                        current_line = "      " + word + " "  # Indent continuation lines
                
                if current_line.strip():
                    wrapped_text.append(current_line.rstrip())
                
                print('\n'.join(wrapped_text))
                print()  # Add spacing between bullet points
        else:
            print("📋 About this item: Not available")
            
        print("=" * 40)
        
        # Ask user if they want to save to JSON
        if ask_save_to_json():
            json_data = prepare_single_product_json(product_details, url)
            generate_json_file(json_data)
    else:
        print("❌ Failed to fetch product details. Please check the URL and try again.")


def display_multiple_products(all_products: list) -> None:
    """
    Display details for multiple products in a summary format.
    
    Args:
        all_products (list): List of tuples containing (url, product_details)
    """
    successful_scrapes = [p for p in all_products if p[1] is not None]
    failed_scrapes = [p for p in all_products if p[1] is None]
    
    print("\n" + "=" * 50)
    print(f"🎯 SCRAPING SUMMARY")
    print("=" * 50)
    print(f"✅ Successfully scraped: {len(successful_scrapes)}/{len(all_products)} products")
    if failed_scrapes:
        print(f"❌ Failed to scrape: {len(failed_scrapes)} products")
    print()
    
    # Display successful scrapes
    for i, (url, product_details) in enumerate(successful_scrapes, 1):
        print(f"📦 PRODUCT {i}")
        print("-" * 20)
        print(f"📝 Title: {product_details['title']}")
        print(f"💰 Price: {product_details['price']}")
        
        if product_details['rating']:
            rating_display = f"⭐ Rating: {product_details['rating']}/5"
            if product_details['num_ratings']:
                rating_display += f" ({product_details['num_ratings']} ratings)"
            print(rating_display)
        
        if product_details['breadcrumbs']:
            breadcrumb_path = " › ".join(product_details['breadcrumbs'])
            print(f"📂 Category: {breadcrumb_path}")
        
        print(f"🔗 URL: {url}")
        
        # Display "About this item" bullet points
        if product_details['about_item']:
            print(f"📋 About this item:")
            for j, bullet in enumerate(product_details['about_item'], 1):
                # Wrap long text for better readability (max 80 characters per line)
                wrapped_text = []
                words = bullet.split(' ')
                current_line = f"   {j}. "
                
                for word in words:
                    if len(current_line + word) <= 80:
                        current_line += word + " "
                    else:
                        wrapped_text.append(current_line.rstrip())
                        current_line = "      " + word + " "  # Indent continuation lines
                
                if current_line.strip():
                    wrapped_text.append(current_line.rstrip())
                
                print('\n'.join(wrapped_text))
        else:
            print("📋 About this item: Not available")
        
        print()
    
    # Display failed scrapes
    if failed_scrapes:
        print("❌ FAILED SCRAPES")
        print("-" * 20)
        for i, (url, _) in enumerate(failed_scrapes, 1):
            print(f"{i}. {url}")
        print()
    
    print("=" * 50)
    
    # Ask user if they want to save to JSON (only if there are successful scrapes)
    if successful_scrapes and ask_save_to_json():
        json_data = prepare_multiple_products_json(all_products)
        generate_json_file(json_data)


def scrape_single_product() -> None:
    """Handle single product scraping workflow."""
    print("\n🔍 Single Product Mode")
    print("=" * 25)
    
    # Get the Amazon product URL from user input
    product_url = input('Enter product URL: ').strip()
    
    # Validate the URL before proceeding
    if not product_url:
        print("❌ Error: Please enter a valid URL.")
        return
    
    if not validate_amazon_url(product_url):
        print("❌ Error: Please enter a valid Amazon product URL.")
        print("   Valid Amazon product URLs should:")
        print("   • Be from an Amazon domain (amazon.com, amazon.co.uk, etc.)")
        return
    
    print("✅ Valid Amazon URL detected!")
    print()  # Add some spacing
    
    # Call the scraping function with loading animation
    product_details = get_product_details_with_loading(product_url)
    
    # Display the scraped product information
    display_single_product(product_details, product_url)


def scrape_multiple_products() -> None:
    """Handle multiple products scraping workflow."""
    print("\n🔍 Multiple Products Mode")
    print("=" * 28)
    
    # Get multiple URLs from user
    urls = get_multiple_urls()
    
    if not urls:
        print("❌ No valid URLs provided.")
        return
    
    print(f"\n✅ Ready to scrape {len(urls)} product(s)!")
    print("🚀 Starting scraping process...\n")
    
    all_products = []
    
    # Scrape each product with progress indication
    for i, url in enumerate(urls, 1):
        print(f"🔄 Processing product {i}/{len(urls)}...")
        
        # Add small delay between requests to be respectful to the server
        if i > 1:
            time.sleep(2)
        
        product_details = get_product_details_with_loading(url, i, len(urls))
        all_products.append((url, product_details))
        
        # Show quick success/failure indication
        if product_details:
            print(f"   ✅ Product {i} scraped successfully!")
        else:
            print(f"   ❌ Product {i} failed to scrape.")
        print()
    
    # Display all results
    display_multiple_products(all_products)


def ask_save_to_json() -> bool:
    """
    Ask user if they want to save scraped data to a JSON file.
    
    Returns:
        bool: True if user wants to save, False otherwise
    """
    print("\n💾 Save scraped data to JSON file?")
    while True:
        choice = input("Would you like to save the scraped data to a JSON file? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("❌ Please enter 'y' for yes or 'n' for no.")


def generate_json_file(data: dict, filename: str = None) -> str:
    """
    Generate a JSON file with scraped product data.
    
    Args:
        data (dict): The scraped data to save
        filename (str): Optional custom filename
        
    Returns:
        str: The filename of the generated JSON file
    """
    if filename is None:
        # Generate timestamp-based filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"amazon_products_{timestamp}.json"
    
    try:
        # Ensure filename has .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        # Write data to JSON file with pretty formatting
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data successfully saved to: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Error saving JSON file: {e}")
        return None


def prepare_single_product_json(product_details: dict, url: str) -> dict:
    """
    Prepare single product data for JSON export.
    
    Args:
        product_details (dict): Product details dictionary
        url (str): Product URL
        
    Returns:
        dict: Formatted data for JSON export
    """
    return {
        "scraping_info": {
            "timestamp": datetime.now().isoformat(),
            "mode": "single_product",
            "total_products": 1,
            "successful_scrapes": 1 if product_details else 0
        },
        "products": [
            {
                "url": url,
                "scraped_successfully": product_details is not None,
                "product_data": product_details if product_details else {}
            }
        ]
    }


def prepare_multiple_products_json(all_products: list) -> dict:
    """
    Prepare multiple products data for JSON export.
    
    Args:
        all_products (list): List of tuples containing (url, product_details)
        
    Returns:
        dict: Formatted data for JSON export
    """
    successful_scrapes = [p for p in all_products if p[1] is not None]
    
    products_data = []
    for url, product_details in all_products:
        products_data.append({
            "url": url,
            "scraped_successfully": product_details is not None,
            "product_data": product_details if product_details else {}
        })
    
    return {
        "scraping_info": {
            "timestamp": datetime.now().isoformat(),
            "mode": "multiple_products",
            "total_products": len(all_products),
            "successful_scrapes": len(successful_scrapes),
            "failed_scrapes": len(all_products) - len(successful_scrapes)
        },
        "products": products_data
    }


# Main execution section
if __name__ == "__main__":
    print("🛒 Amazon Product Scraper")
    print("=" * 30)
    
    # Display configuration menu to choose between single or multiple URL scraping
    mode = display_configuration_menu()
    
    if mode == 1:
        # Single URL mode
        scrape_single_product()
    elif mode == 2:
        # Multiple URLs mode
        scrape_multiple_products()