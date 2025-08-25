"""
Market data notification bot
Sends single combined message to Telegram in English
Order: Gold -> Stocks -> VN-Index -> Exchange -> Crypto
"""
from services.market_data import (
    get_stock_prices, 
    get_vnindex, 
    get_gold_prices, 
    get_exchange_rates, 
    get_crypto_prices
)
from services.telegram_formatter import format_combined_message
from services.telegram_bot import send_to_telegram
from config import (
    STOCK_PRICE_ENABLED, VNINDEX_ENABLED, GOLD_PRICE_ENABLED,
    EXCHANGE_RATE_ENABLED, CRYPTO_PRICE_ENABLED,
    STOCK_SYMBOLS, CRYPTO_SYMBOLS, EXCHANGE_SYMBOLS
)

def main():
    print("Starting Vietnam market data bot...")
    
    # Initialize data variables
    gold_data = None
    stock_data = None
    vnindex_data = None
    exchange_data = None
    crypto_data = None
    
    # 1. Fetch gold prices first
    if GOLD_PRICE_ENABLED:
        print("Fetching SJC gold prices...")
        gold_data = get_gold_prices()
    
    # 2. Fetch stock prices second
    if STOCK_PRICE_ENABLED:
        print("Fetching Vietnamese stock prices...")
        stock_data = get_stock_prices(STOCK_SYMBOLS)
    
    # 3. Fetch VN-Index third
    if VNINDEX_ENABLED:
        print("Fetching VN-Index...")
        vnindex_data = get_vnindex()
    
    # 4. Fetch exchange rates fourth
    if EXCHANGE_RATE_ENABLED:
        print("Fetching VCB exchange rates...")
        exchange_data = get_exchange_rates(EXCHANGE_SYMBOLS)
    
    # 5. Fetch crypto prices fifth
    if CRYPTO_PRICE_ENABLED:
        print("Fetching cryptocurrency prices...")
        crypto_data = get_crypto_prices(CRYPTO_SYMBOLS)
    
    # Format and send single combined message
    message = format_combined_message(
        gold_data, stock_data, vnindex_data, exchange_data, crypto_data
    )
    
    if message:
        print("Sending combined market update to Telegram...")
        send_to_telegram(message)
    else:
        print("No data to send")
    
    print("Vietnam market data bot finished.")

if __name__ == "__main__":
    main()
