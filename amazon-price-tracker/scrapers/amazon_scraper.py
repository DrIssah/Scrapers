# scrapers/amazon_scraper.py
from playwright.sync_api import sync_playwright
import time
import random
from datetime import datetime

class AmazonScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.page = None
        
    def start(self):
        """Launch browser"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.page = self.browser.new_page()
        
        # Set extra headers to avoid detection
        self.page.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def close(self):
        """Close browser"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def get_price(self, url):
        """Get product price from Amazon page"""
        try:
            # Add random delay to avoid detection
            time.sleep(random.uniform(2, 4))
            
            print(f"🔍 Visiting: {url}")
            self.page.goto(url, timeout=30000)
            
            # Try different price selectors Amazon uses
            price_selectors = [
                'span.a-price-whole',
                '.a-price .a-offscreen',
                '#price_inside_buybox',
                '.a-price-range',
                '.a-color-price',
                '#_price.olpWrapper.a-size-small'
            ]

            price_symbol_selectors = [
                'span.a-price-symbol'
            ]
            
            price = None
            price_text = None
            price_symbol =None
            
            for symbol_selector in price_symbol_selectors:
                element = self.page.locator(symbol_selector).first
                if element.count() > 0:
                    price_symbol = element.text_content()
                    if price_symbol:
                        break


            for selector in price_selectors:
                element = self.page.locator(selector).first
                #print(element)
                if element.count() > 0:
                    price_text = element.text_content()
                    if price_text:
                        break
            
            if price_text:
                # Clean up price text
                price_text = price_text.replace('$', '').replace(',', '').strip()
                # Extract first number found
                import re
                print("----------"+price_text)
                price_match = re.search(r'(\d+\.?\d*)', price_text)
                if price_match:
                    price = float(price_match.group(1))
            
            # Get product title - use more specific selector to avoid hidden input with same id
            title = self.page.locator('span#productTitle').first.text_content()
            if title:
                title = title.strip()
            
            return {
                'success': True,
                'price': price,
                'title': title[:50] + '...' if title and len(title) > 50 else title,
                'url': url,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            print(f"❌ Error scraping {url}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'url': url,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

# Simple test function
def test_scraper():
    """Test the scraper with one product"""
    scraper = AmazonScraper(headless=False)  # Set to False so you can see what's happening
    try:
        scraper.start()
        
        # Test with a product
        test_url = "https://www.amazon.com/Sony-WH-1000XM4-Canceling-Headphones-phone-call/dp/B0863TXGM3"
        result = scraper.get_price(test_url)
        
        if result['success']:
            print(f"✅ Success!")
            print(f"📦 Product: {result['title']}")
            print(f"💰 Price: ${result['price']}")
            print(f"🕐 Time: {result['timestamp']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
            
    finally:
        scraper.close()

if __name__ == "__main__":
    test_scraper()