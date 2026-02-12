# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# Products to track - Amazon + Walmart
PRODUCTS = [
    # AMAZON PRODUCTS
    {
        "name": "Sony WH-1000XM4 Headphones",
        "url": "https://www.amazon.com/Sony-WH-1000XM4-Canceling-Headphones-phone-call/dp/B0863TXGM3",
        "target_price": 250.00,
        "site": "Amazon"
    },
    {
        "name": "Amazon Echo Dot (5th Gen)",
        "url": "https://www.amazon.com/Echo-Dot-5th-Gen/dp/B09B8V1LZ3",
        "target_price": 30.00,
        "site": "Amazon"
    },
    
    # WALMART PRODUCTS
    {
        "name": "PlayStation 5 Console",
        "url": "https://www.walmart.com/ip/Sony-PlayStation-5-Console/363472942",
        "target_price": 499.00,
        "site": "Walmart"
    },
    {
        "name": "Xbox Series X",
        "url": "https://www.walmart.com/ip/Xbox-Series-X/443574645",
        "target_price": 499.00,
        "site": "Walmart"
    },
    {
        "name": "LEGO Star Wars Millennium Falcon",
        "url": "https://www.walmart.com/ip/LEGO-Star-Wars-Millennium-Falcon-75257/326316961",
        "target_price": 120.00,
        "site": "Walmart"
    }
]

# Email settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# File paths
DATA_FILE = "data/price_history.csv"
REPORT_FILE = "data/reports/price_report.xlsx"