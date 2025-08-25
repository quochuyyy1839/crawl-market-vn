"""
Market data notification bot
Sends single combined message to Telegram in English
Order: Gold -> Stocks -> VN-Index -> Exchange -> Crypto
"""
from services.core.data_collector import DataCollector
from services.data_sources.stock_service import StockService
from services.data_sources.gold_service import GoldService
from services.data_sources.index_service import IndexService
from services.data_sources.exchange_service import ExchangeService
from services.data_sources.crypto_service import CryptoService
from services.telegram.formatter import format_combined_message
from services.telegram.bot import send_to_telegram
from config.data_sources import (
    STOCK_PRICE_ENABLED, VNINDEX_ENABLED, GOLD_PRICE_ENABLED,
    EXCHANGE_RATE_ENABLED, CRYPTO_PRICE_ENABLED,
    STOCK_SYMBOLS, CRYPTO_SYMBOLS, EXCHANGE_SYMBOLS
)

def main():
    print("Starting Vietnam market data bot...")
    
    # Initialize data collector and services
    collector = DataCollector()
    
    # Register services with their enabled status
    collector.register_service('gold', GoldService(), GOLD_PRICE_ENABLED)
    collector.register_service('stock', StockService(), STOCK_PRICE_ENABLED)
    collector.register_service('vnindex', IndexService(), VNINDEX_ENABLED)
    collector.register_service('exchange', ExchangeService(), EXCHANGE_RATE_ENABLED)
    collector.register_service('crypto', CryptoService(), CRYPTO_PRICE_ENABLED)
    
    # Configure service parameters
    service_configs = {
        'stock': {'symbols': STOCK_SYMBOLS},
        'exchange': {'currencies': EXCHANGE_SYMBOLS},
        'crypto': {'symbols': CRYPTO_SYMBOLS},
        'gold': {},  # No parameters needed
        'vnindex': {}  # No parameters needed
    }
    
    # Collect all data
    results = collector.collect_all(service_configs)
    
    # Format and send single combined message
    message = format_combined_message(
        results.get('gold'), 
        results.get('stock'), 
        results.get('vnindex'), 
        results.get('exchange'), 
        results.get('crypto')
    )
    
    if message:
        print("Sending combined market update to Telegram...")
        send_to_telegram(message)
    else:
        print("No data to send")
    
    print("Vietnam market data bot finished.")

if __name__ == "__main__":
    main()
