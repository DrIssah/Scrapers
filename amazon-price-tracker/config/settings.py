# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# Products to track - YOU CAN EDIT THIS LIST
PRODUCTS = [
    {
        "name": "Sony WH-1000XM4 Headphones",
        "url": "https://www.amazon.com/Sony-WH-1000XM4-Canceling-Headphones-phone-call/dp/B0863TXGM3",
        "target_price": 250.00
    },
    {
        "name": "Amazon Echo Dot (5th Gen)",
        "url": "https://www.amazon.com/Echo-Dot-5th-Gen/dp/B09B8V1LZ3",
        "target_price": 30.00
    },
    {
        "name": "Kindle Paperwhite",
        "url": "https://www.amazon.com/Kindle-Paperwhite-Adjustable-Warm-Light/dp/B08N3LC9J8",
        "target_price": 100.00
    }
]

# Email settings - FILL THIS IN .env file
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# File paths
DATA_FILE = "data/price_history.csv"
REPORT_FILE = "data/reports/price_report.xlsx"