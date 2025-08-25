"""
Market data service using vnstock
"""
from vnstock import Vnstock
from vnstock.explorer.misc import sjc_gold_price, vcb_exchange_rate
from datetime import datetime
import requests
import os

def get_stock_prices(symbols):
    """Get Vietnamese stock prices with full precision"""
    results = []
    for symbol in symbols:
        try:
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            data = stock.quote.history(start='2024-01-01', end='2024-12-31', interval='1D')
            
            if data is not None and len(data) > 0:
                price = data.iloc[-1]['close']
                # Show full price precision
                results.append(f"{symbol}: {price:,.2f} VND")
            else:
                results.append(f"{symbol}: N/A")
        except Exception as e:
            results.append(f"{symbol}: ERROR - {str(e)[:30]}")
    
    return results

def get_vnindex():
    """Get VN-Index with daily changes"""
    try:
        index_obj = Vnstock().world_index(symbol='VNI', source='MSN')
        data = index_obj.quote.history(start='2024-01-01', end='2024-12-31', interval='1D')
        
        if data is not None and len(data) > 0:
            latest = data.iloc[-1]
            prev = data.iloc[-2] if len(data) > 1 else latest
            
            value = latest['close']
            change = latest['close'] - prev['close'] 
            change_percent = (change / prev['close']) * 100
            
            change_sign = "+" if change >= 0 else ""
            return f"VN-Index: {value:,.2f} ({change_sign}{change:,.2f}, {change_percent:+.2f}%)"
        else:
            return "VN-Index: N/A"
    except Exception as e:
        return f"VN-Index: ERROR - {str(e)[:50]}"

def get_gold_prices():
    """Get SJC gold prices with full error logging"""
    try:
        gold_data = sjc_gold_price()
        if gold_data is not None and len(gold_data) > 0:
            sjc_row = gold_data.iloc[0]
            buy_price = sjc_row.get('buy_price', 'N/A')
            sell_price = sjc_row.get('sell_price', 'N/A')
            
            if buy_price != 'N/A' and sell_price != 'N/A':
                buy_formatted = f"{buy_price/1000:,.0f}k"
                sell_formatted = f"{sell_price/1000:,.0f}k"
                return f"SJC Gold: Buy {buy_formatted} - Sell {sell_formatted}"
            else:
                return f"SJC Gold: Buy {buy_price} - Sell {sell_price}"
        else:
            return "SJC Gold: No data available"
    except Exception as e:
        # Return full error for debugging
        import traceback
        error_details = traceback.format_exc()
        return f"SJC Gold: ERROR - {str(e)} | Details: {error_details[:100]}"

def get_exchange_rates(currencies):
    """Get VCB exchange rates with buy/sell"""
    results = []
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        rate_data = vcb_exchange_rate(date=today)
        
        if rate_data is not None and len(rate_data) > 0:
            for currency in currencies:
                currency_row = rate_data[rate_data['currency_code'] == currency]
                if len(currency_row) > 0:
                    row = currency_row.iloc[0]
                    buy = row.get('buy _transfer', 'N/A') 
                    sell = row.get('sell', 'N/A')
                    results.append(f"{currency}: Buy {buy} - Sell {sell}")
                else:
                    results.append(f"{currency}: N/A")
        else:
            results.append("Exchange rates: No data available")
    except Exception as e:
        results.append(f"Exchange rates: ERROR - {str(e)[:50]}")
    
    return results

def get_crypto_prices(symbols):
    """Get cryptocurrency prices from CoinGecko"""
    results = []
    try:
        # Map symbols to CoinGecko IDs
        crypto_map = {'BTC': 'bitcoin', 'ETH': 'ethereum'}
        ids = [crypto_map.get(s) for s in symbols if s in crypto_map]
        
        if not ids:
            return ["Crypto: No valid symbols"]
        
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&vs_currencies=usd&include_24hr_change=true"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            for symbol in symbols:
                crypto_id = crypto_map.get(symbol)
                if crypto_id and crypto_id in data:
                    price = data[crypto_id]['usd']
                    change_24h = data[crypto_id].get('usd_24h_change', 0)
                    
                    change_sign = "+" if change_24h >= 0 else ""
                    results.append(f"{symbol}: ${price:,.2f} ({change_sign}{change_24h:.2f}%)")
                else:
                    results.append(f"{symbol}: N/A")
        else:
            results.append(f"Crypto: API error {response.status_code}")
            
    except Exception as e:
        results.append(f"Crypto: ERROR - {str(e)[:50]}")
    
    return results