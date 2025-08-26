"""
Main configuration settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Config
TOKEN = os.getenv('TOKEN', '')
CHAT_ID = os.getenv('CHAT_ID', '')
TELEGRAM_ENABLED = os.getenv('TELEGRAM_ENABLED', 'false').lower() == 'true'

# Telegram URL
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"