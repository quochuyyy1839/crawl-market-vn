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
                # Format VND price with k notation for all stock prices
                price_formatted = f"{price:,.1f}k VND"
                results.append(f"{symbol}: {price_formatted}")
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
                buy_formatted = f"{buy_price/1000:,.0f}k VND"
                sell_formatted = f"{sell_price/1000:,.0f}k VND"
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
                    
                    # Format exchange rates with k notation
                    try:
                        # Clean string: remove commas used as thousand separators
                        buy_clean = str(buy).replace(',', '') if buy != 'N/A' else '0'
                        buy_num = float(buy_clean)
                        buy_formatted = f"{buy_num/1000:,.1f}k VND" if buy_num > 0 else str(buy)
                    except (ValueError, TypeError):
                        buy_formatted = str(buy)
                    
                    try:
                        # Clean string: remove commas used as thousand separators  
                        sell_clean = str(sell).replace(',', '') if sell != 'N/A' else '0'
                        sell_num = float(sell_clean)
                        sell_formatted = f"{sell_num/1000:,.1f}k VND" if sell_num > 0 else str(sell)
                    except (ValueError, TypeError):
                        sell_formatted = str(sell)
                    
                    results.append(f"{currency}: Buy {buy_formatted} - Sell {sell_formatted}")
                else:
                    results.append(f"{currency}: N/A")
        else:
            results.append("Exchange rates: No data available")
    except Exception as e:
        results.append(f"Exchange rates: ERROR - {str(e)[:50]}")
    
    return results

def get_crypto_prices(symbols):
    """Get cryptocurrency prices from CoinGecko with auto-detection"""
    results = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        # Auto-detect coin IDs by searching CoinGecko
        coin_ids = []
        for symbol in symbols:
            search_url = f"https://api.coingecko.com/api/v3/search?query={symbol}"
            search_response = requests.get(search_url, headers=headers, timeout=10)
            
            if search_response.status_code == 200:
                search_data = search_response.json()
                coins = search_data.get('coins', [])
                
                # Find exact symbol match
                for coin in coins:
                    if coin.get('symbol', '').upper() == symbol.upper():
                        coin_ids.append(coin.get('id'))
                        break
        
        if not coin_ids:
            return ["Crypto: No coins found"]
        
        # Get prices for detected coins (both USD and VND)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coin_ids)}&vs_currencies=usd,vnd&include_24hr_change=true"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Match results back to original symbols
            for i, symbol in enumerate(symbols):
                if i < len(coin_ids) and coin_ids[i] in data:
                    coin_data = data[coin_ids[i]]
                    usd_price = coin_data.get('usd', 0)
                    vnd_price = coin_data.get('vnd', 0)
                    change_24h = coin_data.get('usd_24h_change', 0)
                    
                    change_sign = "+" if change_24h >= 0 else ""
                    
                    # Format VND price
                    if vnd_price > 1000000:
                        vnd_formatted = f"{vnd_price/1000000:,.1f}M VND"
                    elif vnd_price > 1000:
                        vnd_formatted = f"{vnd_price/1000:,.0f}k VND"
                    else:
                        vnd_formatted = f"{vnd_price:,.0f} VND"
                    
                    results.append(f"{symbol}: ${usd_price:,.2f} / {vnd_formatted} ({change_sign}{change_24h:.2f}%)")
                else:
                    results.append(f"{symbol}: N/A")
        else:
            results.append(f"Crypto: API error {response.status_code}")
            
    except Exception as e:
        results.append(f"Crypto: ERROR - {str(e)[:50]}")
    
    return results