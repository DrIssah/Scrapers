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
        "name": "Anker Nano USB C Wall Charger, 45W Fast Charging Smart",
        "url": "https://www.amazon.com/Anker-Charging-Foldable-Recognition-Non-Battery/dp/B0G1MRLXMV",
        "target_price": 300.00
    },
    {
        "name": "Gaming Laptop, 15.6inch Laptop with AMD Ryzen 7",
        "url": "https://www.amazon.com/KAIGERR-15-6inch-Performance-Computer-Graphics/dp/B0GD61F6FC",
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