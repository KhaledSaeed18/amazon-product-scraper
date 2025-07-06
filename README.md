# 🛒 Amazon Product Scraper

[![Python](https://img.shields.io/badge/Python-3.10.7-blue.svg)](https://www.python.org/downloads/)
[![Dependencies](https://img.shields.io/badge/Dependencies-requests%20%7C%20beautifulsoup4%20%7C%20lxml-orange.svg)](requirements.txt)

A comprehensive Python web scraper that extracts detailed product information from Amazon product pages using Beautiful Soup and requests. This tool mimics browser behavior to avoid being blocked and provides an intuitive command-line interface for scraping single or multiple products.

## 📋 Table of Contents

- [✨ Features](#-features)
- [🌐 Supported Domains](#-supported-amazon-domains)
- [📋 Requirements](#-requirements)
- [🚀 Installation](#-installation)
- [🎮 Usage](#-usage)
- [📊 Sample Output](#-sample-output)
- [💾 JSON Export](#-json-export-format)
- [🔧 Technical Details](#-technical-details)

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

| Country | Domain | Status |
|---------|--------|--------|
| United States | amazon.com | ✅ |
| United Kingdom | amazon.co.uk | ✅ |
| Canada | amazon.ca | ✅ |
| Germany | amazon.de | ✅ |
| France | amazon.fr | ✅ |
| Italy | amazon.it | ✅ |
| Spain | amazon.es | ✅ |
| India | amazon.in | ✅ |
| Japan | amazon.co.jp | ✅ |
| Australia | amazon.com.au | ✅ |

## 📋 Requirements

- **Python**: 3.7 or higher
- **Internet Connection**: Required for web scraping
- **Dependencies**: Listed in `requirements.txt`

## 🚀 Installation

### Method 1: Quick Setup

```bash
# Clone the repository
git clone https://github.com/KhaledSaeed18/amazon-product-scraper.git
cd amazon-product-scraper

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Manual Setup

1. **Download the Project**

   ```bash
   # Download as ZIP or clone
   git clone https://github.com/KhaledSaeed18/amazon-product-scraper.git
   ```

2. **Create Virtual Environment**

   ```bash
   cd amazon-product-scraper
   python -m venv venv
   ```

3. **Activate Virtual Environment**

   ```bash
   # Windows Command Prompt
   venv\Scripts\activate.bat
   
   # Windows PowerShell
   venv\Scripts\Activate.ps1
   
   # Mac/Linux
   source venv/bin/activate
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

### Quick Start

```bash
python scraper.py
```

### Interactive Menu

The scraper presents an interactive menu with two options:

```bash
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

**Supported URL formats:**

```bash
https://www.amazon.com/dp/B08N5WRWNW
https://amazon.co.uk/gp/product/B08N5WRWNW
https://www.amazon.de/dp/B08N5WRWNW
https://amazon.com/Some-Product-Name/dp/B08N5WRWNW
```

### Multiple Products Mode

1. Select option `2` for bulk scraping
2. Enter multiple Amazon product URLs (one per line)
3. Press Enter twice when finished entering URLs
4. Monitor progress as each product is scraped
5. View comprehensive summary of all products
6. Optionally save all results to JSON file

**Tips for Multiple Products:**

- Add 2-3 second delays between requests (built-in)
- Maximum recommended: 50 products per session
- URLs are validated before processing

## 📊 Sample Output

### Single Product Output

```bash
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

```bash
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

| Data Point | CSS Selector/Method | Fallback |
|------------|---------------------|----------|
| Product Title | `span#productTitle` | N/A |
| Price | `span.a-price` | "Not available" |
| Rating | `i.a-icon-star` elements | "Not available" |
| Review Count | `span#acrCustomerReviewText` | "Not available" |
| Product Image | `img#landingImage` | "Not available" |
| Categories | Breadcrumb navigation | Empty array |
| Features | "About this item" bullets | Empty array |

---

**Happy Scraping! 🚀**
