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
from config.settings import TELEGRAM_ENABLED
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
    
    # Print collected data to console
    print("\n" + "="*60)
    print("COLLECTED MARKET DATA:")
    print("="*60)
    
    if results.get('gold'):
        print(f"🥇 GOLD: {results['gold']}")
    
    if results.get('stock'):
        print("📈 STOCKS:")
        for stock in results['stock']:
            print(f"   {stock}")
    
    if results.get('vnindex'):
        print(f"📊 VN-INDEX: {results['vnindex']}")
    
    if results.get('exchange'):
        print("💱 EXCHANGE:")
        for rate in results['exchange']:
            print(f"   {rate}")
    
    if results.get('crypto'):
        print("₿ CRYPTO:")
        for crypto in results['crypto']:
            print(f"   {crypto}")
    
    print("="*60)
    
    # Format and send message to Telegram if enabled
    message = format_combined_message(
        results.get('gold'), 
        results.get('stock'), 
        results.get('vnindex'), 
        results.get('exchange'), 
        results.get('crypto')
    )
    
    if message:
        if TELEGRAM_ENABLED:
            print("\nSending combined market update to Telegram...")
            send_to_telegram(message)
    else:
        print("No data to send")
    
    print("Vietnam market data bot finished.")

if __name__ == "__main__":
    main()
