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

# Telegram URL
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"