"""
Configuration loader from .env file
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Config
TOKEN = os.getenv('TOKEN', '')
CHAT_ID = os.getenv('CHAT_ID', '')

# Feature Toggles
STOCK_PRICE_ENABLED = os.getenv('STOCK_PRICE', 'false').lower() == 'true'
VNINDEX_ENABLED = os.getenv('VNINDEX', 'false').lower() == 'true'
GOLD_PRICE_ENABLED = os.getenv('GOLD_PRICE', 'false').lower() == 'true'
EXCHANGE_RATE_ENABLED = os.getenv('EXCHANGE_RATE', 'false').lower() == 'true'
CRYPTO_PRICE_ENABLED = os.getenv('CRYPTO_PRICE', 'false').lower() == 'true'

# Symbols
STOCK_SYMBOLS = os.getenv('STOCK', 'VCB,VIC,HPG').split(',')
GOLD_SYMBOLS = os.getenv('GOLD', 'SJC').split(',')
CRYPTO_SYMBOLS = os.getenv('CRYPTO', 'BTC,ETH').split(',')
EXCHANGE_SYMBOLS = os.getenv('EXCHANGE', 'USD,EUR,JPY').split(',')

# Clean up symbols (remove whitespace)
STOCK_SYMBOLS = [s.strip() for s in STOCK_SYMBOLS]
GOLD_SYMBOLS = [s.strip() for s in GOLD_SYMBOLS]
CRYPTO_SYMBOLS = [s.strip() for s in CRYPTO_SYMBOLS]
EXCHANGE_SYMBOLS = [s.strip() for s in EXCHANGE_SYMBOLS]

# Telegram URL
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"