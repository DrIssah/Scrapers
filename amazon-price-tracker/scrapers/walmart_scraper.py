# scrapers/walmart_scraper.py
import re
from datetime import datetime
from utils.anti_detection import (
    BrowserLauncher, 
    PageValidator, 
    AntiDetection, 
    ScraperHelper
)

class WalmartScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.page = None
        self.playwright = None
        
    def start(self):
        """Launch Chromium browser"""
        self.playwright, self.browser, self.page = BrowserLauncher.launch_chromium(
            headless=self.headless
        )
        
    def close(self):
        """Close browser"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def get_price(self, url):
        """Get product price from Walmart"""
        try:
            # Simple delay
            AntiDetection.human_delay(2, 4)
            
            # Go to page
            self.page.goto(url, timeout=30000)
            
            # Check if blocked
            if PageValidator.is_blocked(self.page):
                return {'success': False, 'error': 'Blocked', 'site': 'Walmart'}
            
            # Try price selectors
            price_selectors = [
                '[data-automation-id="product-price"]',
                '[itemprop="price"]',
                '.price-now',
                '.prod-price'
            ]
            
            price = None
            for selector in price_selectors:
                element = self.page.locator(selector).first
                if element.count() > 0:
                    price_text = element.text_content()
                    if price_text:
                        # Extract number
                        price_match = re.search(r'(\d+\.?\d*)', price_text)
                        if price_match:
                            price = float(price_match.group(1))
                            break
            
            # Get title
            title = self.page.locator('h1').first.text_content()
            
            if price:
                return {
                    'success': True,
                    'price': price,
                    'title': title[:50] + '...' if title and len(title) > 50 else title,
                    'url': url,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'site': 'Walmart'
                }
            else:
                return {'success': False, 'error': 'Price not found', 'site': 'Walmart'}
                
        except Exception as e:
            return {'success': False, 'error': str(e), 'site': 'Walmart'}

# Test
def test_scraper():
    scraper = WalmartScraper(headless=False)
    try:
        scraper.start()
        url = "https://www.walmart.com/ip/Sony-PlayStation-5-Console/363472942"
        result = scraper.get_price(url)
        
        if result['success']:
            print(f"✅ ${result['price']} - {result['title']}")
        else:
            print(f"❌ {result['error']}")
    finally:
        scraper.close()

if __name__ == "__main__":
    test_scraper()