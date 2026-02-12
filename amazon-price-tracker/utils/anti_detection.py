# utils/anti_detection.py
from playwright.sync_api import sync_playwright, TimeoutError
import random
import time

class AntiDetection:
    """Anti-detection strategies for web scraping"""
    
    @staticmethod
    def get_random_user_agent():
        """Return random user agent"""
        user_agents = [
            # Windows Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            
            # Windows Firefox
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0',
            
            # Mac Chrome
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            
            # Mac Safari
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        ]
        return random.choice(user_agents)
    
    @staticmethod
    def get_random_viewport():
        """Return random viewport size"""
        viewports = [
            {'width': 1920, 'height': 1080},
            {'width': 1366, 'height': 768},
            {'width': 1536, 'height': 864},
            {'width': 1440, 'height': 900},
            {'width': 1280, 'height': 720},
        ]
        return random.choice(viewports)
    
    @staticmethod
    def human_delay(min_seconds=1, max_seconds=3):
        """Random delay to mimic human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        return delay
    
    @staticmethod
    def random_scroll(page):
        """Randomly scroll page like a human"""
        try:
            # Get page height
            page_height = page.evaluate('document.body.scrollHeight')
            
            # Random scroll position (20% to 80% of page)
            scroll_position = random.randint(int(page_height * 0.2), int(page_height * 0.8))
            
            # Smooth scroll
            page.evaluate(f'window.scrollTo({{top: {scroll_position}, behavior: "smooth"}})')
            
            # Wait a bit
            time.sleep(random.uniform(0.5, 1.5))
        except:
            pass


class PageValidator:
    """Validate page state and detect blocks"""
    
    @staticmethod
    def is_blocked(page):
        """Check if page shows bot detection"""
        try:
            page_text = page.content().lower()
            
            # Common bot detection indicators
            blocked_indicators = [
                'robot',
                'human',
                'verify you are human',
                'captcha',
                'access denied',
                'unusual traffic',
                'please confirm',
                'security check',
                'automated access',
                'too many requests',
                '403 forbidden',
                'blocked',
                'ddos',
                'bot detected'
            ]
            
            # Check page text
            for indicator in blocked_indicators:
                if indicator in page_text:
                    print(f"⚠️ Block detected: '{indicator}'")
                    return True
            
            # Check URL for redirects to bot pages
            current_url = page.url.lower()
            blocked_urls = ['captcha', 'robot', 'verify', 'denied', 'blocked']
            for blocked in blocked_urls:
                if blocked in current_url:
                    print(f"⚠️ Redirect to bot page: {current_url}")
                    return True
            
            return False
            
        except:
            return False
    
    @staticmethod
    def wait_for_stable_network(page, timeout=10000):
        """Wait for network to be idle"""
        try:
            page.wait_for_load_state('networkidle', timeout=timeout)
            return True
        except TimeoutError:
            print("⚠️ Network idle timeout")
            return False
    
    @staticmethod
    def page_has_content(page):
        """Check if page actually has product content"""
        try:
            # Check for common content indicators
            content_indicators = [
                'price',
                'product',
                'add to cart',
                'buy now',
                'item',
                'in stock'
            ]
            
            page_text = page.content().lower()
            for indicator in content_indicators:
                if indicator in page_text:
                    return True
            return False
        except:
            return False


class BrowserLauncher:
    """Launch browsers with anti-detection configs"""
    
    @staticmethod
    def launch_chromium(headless=True, use_stealth=True):
        """Launch Chromium with anti-detection args"""
        playwright = sync_playwright().start()
        
        args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-site-isolation-trials',
        ]
        
        if use_stealth:
            args.extend([
                '--disable-automation',
                '--disable-infobars',
            ])
        
        browser = playwright.chromium.launch(
            headless=headless,
            args=args
        )
        
        context = browser.new_context(
            viewport=AntiDetection.get_random_viewport(),
            user_agent=AntiDetection.get_random_user_agent(),
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation'],
            device_scale_factor=1,
            has_touch=False
        )
        
        page = context.new_page()
        
        # Stealth: remove webdriver property
        if use_stealth:
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
            """)
        
        return playwright, browser, page
    
    @staticmethod
    def launch_firefox(headless=True):
        """Launch Firefox (good for Walmart)"""
        playwright = sync_playwright().start()
        
        browser = playwright.firefox.launch(
            headless=headless
        )
        
        context = browser.new_context(
            viewport=AntiDetection.get_random_viewport(),
            user_agent=AntiDetection.get_random_user_agent(),
            locale='en-US'
        )
        
        page = context.new_page()
        return playwright, browser, page
    
    @staticmethod
    def launch_webkit(headless=True):
        """Launch WebKit/Safari"""
        playwright = sync_playwright().start()
        
        browser = playwright.webkit.launch(
            headless=headless
        )
        
        context = browser.new_context(
            viewport=AntiDetection.get_random_viewport(),
            user_agent=AntiDetection.get_random_user_agent(),
            locale='en-US'
        )
        
        page = context.new_page()
        return playwright, browser, page


class ScraperHelper:
    """Helper methods for scrapers"""
    
    @staticmethod
    def safe_goto(page, url, timeout=30000):
        """Navigate to URL with error handling"""
        try:
            response = page.goto(url, timeout=timeout, wait_until='commit')
            
            if response and response.status >= 400:
                print(f"⚠️ HTTP {response.status}: {url}")
                return False
                
            return True
        except TimeoutError:
            print(f"⚠️ Timeout: {url}")
            return False
        except Exception as e:
            print(f"⚠️ Navigation error: {str(e)}")
            return False
    
    @staticmethod
    def retry_on_failure(func, max_retries=3, delay=2):
        """Retry function on failure"""
        for attempt in range(max_retries):
            try:
                result = func()
                if result and result.get('success'):
                    return result
                else:
                    print(f"🔄 Retry {attempt + 1}/{max_retries}...")
                    time.sleep(delay * (attempt + 1))  # Exponential backoff
            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(delay * (attempt + 1))
        
        return {'success': False, 'error': 'Max retries exceeded'}