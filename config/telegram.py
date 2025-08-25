"""
Telegram specific configurations
"""
from .settings import TOKEN, CHAT_ID, TELEGRAM_URL

# Re-export telegram configurations for easy access
__all__ = ['TOKEN', 'CHAT_ID', 'TELEGRAM_URL']