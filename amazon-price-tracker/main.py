# main.py
import pandas as pd
from datetime import datetime
import os
from scrapers.amazon_scraper import AmazonScraper
from config.settings import PRODUCTS, DATA_FILE

def load_existing_data():
    """Load existing price history if it exists"""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=['timestamp', 'product_name', 'price', 'url', 'target_price'])

def save_data(new_data):
    """Save price data to CSV"""
    df = load_existing_data()
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    print(f"💾 Data saved to {DATA_FILE}")
    return df

def check_price_alert(price, target_price, product_name):
    """Check if price is below target"""
    if price and target_price and price <= target_price:
        print(f"🔔 ALERT! {product_name} is ${price} (below target ${target_price})")
        return True
    return False

def main():
    print("🚀 Starting Amazon Price Tracker...")
    
    scraper = AmazonScraper(headless=False)
    
    try:
        scraper.start()
        
        for product in PRODUCTS:
            print(f"\n{'='*50}")
            print(f"Checking: {product['name']}")
            
            result = scraper.get_price(product['url'])
            
            if result['success']:
                # Prepare data for saving
                price_data = {
                    'timestamp': result['timestamp'],
                    'product_name': product['name'],
                    'price': result['price'],
                    'url': product['url'],
                    'target_price': product['target_price']
                }
                
                # Save to CSV
                df = save_data(price_data)
                
                # Check for alerts
                check_price_alert(
                    result['price'], 
                    product['target_price'], 
                    product['name']
                )
            else:
                print(f"❌ Could not get price for {product['name']}")
            
            # Wait between products
            import time
            time.sleep(3)
            
    finally:
        scraper.close()
    
    print("\n✅ Price tracking complete!")
    
    # Show summary
    df = load_existing_data()
    print(f"\n📊 Total records: {len(df)}")
    if len(df) > 0:
        print(f"Latest prices:")
        latest = df.groupby('product_name').last().reset_index()
        for _, row in latest.iterrows():
            print(f"  • {row['product_name']}: ${row['price']:.2f}")

if __name__ == "__main__":
    main()