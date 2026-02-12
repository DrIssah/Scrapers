# main.py
import pandas as pd
from datetime import datetime
import os
import time
from scrapers.amazon_scraper import AmazonScraper
from scrapers.walmart_scraper import WalmartScraper
from config.settings import PRODUCTS, DATA_FILE

def load_existing_data():
    """Load existing price history if it exists"""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=['timestamp', 'product_name', 'price', 'url', 'target_price', 'site'])

def save_data(new_data):
    """Save price data to CSV"""
    df = load_existing_data()
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    print(f"💾 Data saved to {DATA_FILE}")

def check_price_alert(price, target_price, product_name, site):
    """Check if price is below target"""
    if price and target_price and price <= target_price:
        print(f"🔔 ALERT! {site} - {product_name} is ${price:.2f} (below target ${target_price:.2f})")
        return True
    return False

def main():
    print("🚀 Starting Multi-Site Price Tracker...")
    print(f"📊 Tracking {len(PRODUCTS)} products across Amazon & Walmart\n")
    
    # Initialize scrapers
    amazon = AmazonScraper(headless=True)
    walmart = WalmartScraper(headless=True)
    
    try:
        amazon.start()
        walmart.start()
        
        for product in PRODUCTS:
            print(f"{'='*60}")
            print(f"Checking: {product['name']}")
            print(f"🏬 Store: {product['site']}")
            
            # Choose correct scraper
            if product['site'] == 'Amazon':
                result = amazon.get_price(product['url'])
            elif product['site'] == 'Walmart':
                result = walmart.get_price(product['url'])
            else:
                print(f"❌ Unknown site: {product['site']}")
                continue
            
            if result['success'] and result['price']:
                # Prepare data for saving
                price_data = {
                    'timestamp': result['timestamp'],
                    'product_name': product['name'],
                    'price': result['price'],
                    'url': product['url'],
                    'target_price': product['target_price'],
                    'site': product['site']
                }
                
                # Save to CSV
                save_data(price_data)
                
                # Check for alerts
                check_price_alert(
                    result['price'], 
                    product['target_price'], 
                    product['name'],
                    product['site']
                )
                
                print(f"💰 Price: ${result['price']:.2f}")
            else:
                print(f"❌ Could not get price")
            
            # Wait between products
            time.sleep(3)
            
    finally:
        amazon.close()
        walmart.close()
    
    print(f"\n{'='*60}")
    print("✅ Price tracking complete!")
    
    # Show summary
    df = load_existing_data()
    print(f"\n📊 Total records in database: {len(df)}")
    
    if len(df) > 0:
        print("\n📈 Latest prices by store:")
        latest = df.groupby('product_name').last().reset_index()
        for _, row in latest.iterrows():
            print(f"  • [{row['site']}] {row['product_name']}: ${row['price']:.2f}")

if __name__ == "__main__":
    main()