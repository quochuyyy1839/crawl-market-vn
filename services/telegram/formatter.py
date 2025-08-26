"""
Telegram message formatter - Single message with English format
"""
from datetime import datetime

def format_combined_message(gold_data, stock_data, vnindex_data, exchange_data, crypto_data):
    """Format all market data into single English message"""
    message = "*📊 VIETNAM MARKET UPDATE*\n\n"
    
    # 1. Gold prices first
    if gold_data:
        message += "🥇 *GOLD PRICES*\n```\n"
        message += f"{gold_data}\n"
        message += "```\n\n"
    
    # 2. Stock prices second  
    if stock_data:
        message += "📈 *VIETNAMESE STOCKS*\n```\n"
        for stock_info in stock_data:
            message += f"{stock_info}\n"
        message += "```\n\n"
    
    # 3. VN-Index third
    if vnindex_data:
        message += "📊 *MARKET INDEX*\n```\n"
        message += f"{vnindex_data}\n"
        message += "```\n\n"
    
    # 4. Exchange rates fourth
    if exchange_data:
        message += "💱 *VCB EXCHANGE RATES*\n```\n"
        for rate_info in exchange_data:
            message += f"{rate_info}\n"
        message += "```\n\n"
    
    # 5. Cryptocurrency fifth
    if crypto_data:
        message += "₿ *CRYPTOCURRENCY*\n```\n"
        for crypto_info in crypto_data:
            message += f"{crypto_info}\n"
        message += "```\n\n"
    
    # Add timestamp in UTC+7
    from datetime import timedelta
    utc_now = datetime.utcnow()
    vietnam_time = utc_now + timedelta(hours=7)
    now = vietnam_time.strftime('%d/%m/%Y %H:%M:%S')
    message += f"_Updated: {now} (UTC+7)_"
    
    return message

# Keep individual formatters for compatibility if needed
def add_timestamp_footer():
    """Add timestamp footer"""
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    return f"\n_Updated: {now}_"