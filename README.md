# 🛒 Amazon Product Scraper

A comprehensive Python web scraper that extracts detailed product information from Amazon product pages using Beautiful Soup and requests. This tool mimics browser behavior to avoid being blocked and provides an intuitive command-line interface for scraping single or multiple products.

## ✨ Features

### 🎯 Core Functionality

- **Single Product Scraping**: Extract detailed information from a single Amazon product
- **Bulk Product Scraping**: Process multiple Amazon URLs in one session
- **Comprehensive Data Extraction**: Scrapes multiple data points including:
  - Product title
  - Price information
  - Customer ratings and review counts
  - Product images (high-resolution URLs)
  - Product categories (breadcrumb navigation)
  - "About this item" bullet points
  - Product URLs

### 🔧 Advanced Features

- **Smart URL Validation**: Validates Amazon URLs across multiple international domains
- **Loading Animations**: Beautiful spinner animations during scraping operations
- **Progress Tracking**: Real-time progress indicators for bulk operations
- **Error Handling**: Robust error handling with detailed feedback
- **Data Export**: JSON export functionality with timestamps
- **Rate Limiting**: Built-in delays between requests to respect server resources
- **Multi-domain Support**: Works with Amazon domains worldwide (US, UK, CA, DE, FR, IT, ES, IN, JP, AU)

### 🌐 Supported Amazon Domains

- amazon.com (United States)
- amazon.co.uk (United Kingdom)
- amazon.ca (Canada)
- amazon.de (Germany)
- amazon.fr (France)
- amazon.it (Italy)
- amazon.es (Spain)
- amazon.in (India)
- amazon.co.jp (Japan)
- amazon.com.au (Australia)

## 📋 Requirements

- Python 3.7+
- Internet connection
- Dependencies listed in `requirements.txt`

## 🚀 Installation

### 1. Clone or Download the Project

```bash
git clone https://github.com/KhaledSaeed18/amazon-product-scraper.git
cd amazon-product-scraper
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Running the Scraper

```bash
python scraper.py
```

### Interactive Menu

The scraper presents an interactive menu with two options:

```
🛒 Amazon Product Scraper - Configuration
=============================================

📋 Choose scraping mode:
   1️⃣  Single Product URL
   2️⃣  Multiple Product URLs

Select option (1 or 2):
```

### Single Product Mode

1. Select option `1` for single product scraping
2. Enter a valid Amazon product URL
3. Wait for the scraping process to complete
4. View the detailed product information
5. Optionally save results to JSON file

**Example URL formats:**

```
https://www.amazon.com/dp/B08N5WRWNW
https://amazon.co.uk/gp/product/B08N5WRWNW
https://www.amazon.de/dp/B08N5WRWNW
```

### Multiple Products Mode

1. Select option `2` for bulk scraping
2. Enter multiple Amazon product URLs (one per line)
3. Press Enter twice when finished entering URLs
4. Monitor progress as each product is scraped
5. View comprehensive summary of all products
6. Optionally save all results to JSON file

## 📊 Sample Output

### Single Product Output

```
✅ Product details fetched successfully!
========================================
📝 Title: Echo Dot (4th Gen) | Smart speaker with Alexa | Charcoal
💰 Price: $49.99
📂 Category: Electronics › Smart Home › Smart Speakers
⭐ Rating: 4.7/5 (125,432 ratings)
🖼️  Image: https://m.media-amazon.com/images/I/714Rd3c42AL._AC_SL1500_.jpg
🔗 URL: https://www.amazon.com/dp/B07FZ8S74R

📋 About this item:
   1. Meet Echo Dot - Our most popular smart speaker with a fabric 
      design. It is our most compact smart speaker that fits 
      perfectly into small spaces.
   
   2. Improved speaker quality - Better speaker quality than Echo Dot 
      Gen 2 for richer and louder sound. Pair with a second Echo Dot 
      for stereo sound.
```

### Multiple Products Summary

```
==================================================
🎯 SCRAPING SUMMARY
==================================================
✅ Successfully scraped: 3/3 products

📦 PRODUCT 1
--------------------
📝 Title: Echo Dot (4th Gen) | Smart speaker with Alexa | Charcoal
💰 Price: $49.99
⭐ Rating: 4.7/5 (125,432 ratings)
📂 Category: Electronics › Smart Home › Smart Speakers
🔗 URL: https://www.amazon.com/dp/B07FZ8S74R
```

## 💾 JSON Export Format

When saving data to JSON, the file includes comprehensive metadata:

```json
{
  "scraping_info": {
    "timestamp": "2025-07-04T10:30:00.000000",
    "mode": "single_product",
    "total_products": 1,
    "successful_scrapes": 1
  },
  "products": [
    {
      "url": "https://www.amazon.com/dp/B07FZ8S74R",
      "scraped_successfully": true,
      "product_data": {
        "title": "Echo Dot (4th Gen) | Smart speaker with Alexa | Charcoal",
        "price": "$49.99",
        "rating": "4.7",
        "num_ratings": "125,432",
        "image_url": "https://m.media-amazon.com/images/I/714Rd3c42AL._AC_SL1500_.jpg",
        "about_item": [
          "Meet Echo Dot - Our most popular smart speaker...",
          "Improved speaker quality - Better speaker quality..."
        ],
        "breadcrumbs": [
          "Electronics",
          "Smart Home",
          "Smart Speakers"
        ]
      }
    }
  ]
}
```

## 🔧 Technical Details

### Web Scraping Strategy

- **User-Agent Spoofing**: Mimics Chrome browser to avoid detection
- **Request Headers**: Includes proper Accept-Language headers
- **HTML Parsing**: Uses lxml parser for optimal performance
- **Element Targeting**: Uses specific CSS selectors and IDs for reliable data extraction

### Error Handling

- **URL Validation**: Comprehensive validation for Amazon URLs
- **Network Errors**: Graceful handling of connection issues
- **Missing Elements**: Safe extraction with fallback values

### Data Extraction Points

The scraper extracts the following information:

- **Product Title**: From `span#productTitle`
- **Price**: From `span.a-price`
- **Rating**: From `i.a-icon-star` elements
- **Review Count**: From `span#acrCustomerReviewText`
- **Product Image**: From `img#landingImage` (high-res when available)
- **Categories**: From breadcrumb navigation
- **Features**: From "About this item" bullet points

**Happy Scraping! 🚀**
