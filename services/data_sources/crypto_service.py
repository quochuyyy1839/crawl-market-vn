"""
Cryptocurrency price service using Binance API
"""
from typing import List
import requests
from ..core.base_service import BaseMarketDataService

class CryptoService(BaseMarketDataService):
    """Service for fetching cryptocurrency prices from Binance"""
    
    def __init__(self):
        super().__init__("Cryptocurrency")
    
    def fetch_data(self, symbols: List[str]) -> List[str]:
        """Get cryptocurrency prices from Binance API with real-time USD/VND rate"""
        results = []
        
        try:
            # Get all tickers from Binance in one request
            ticker_url = "https://api.binance.com/api/v3/ticker/24hr"
            response = requests.get(ticker_url, timeout=10)
            
            if response.status_code != 200:
                results.append(f"Crypto: Binance API error {response.status_code}")
                return results
            
            all_tickers = response.json()
            
            # Create a mapping of symbols to data
            ticker_map = {}
            usd_to_vnd = None
            
            for ticker in all_tickers:
                symbol = ticker['symbol']
                if symbol.endswith('USDT'):
                    base_symbol = symbol.replace('USDT', '')
                    ticker_map[base_symbol] = ticker
                # Get real-time USD/VND rate
                elif symbol == 'USDTVND' or symbol == 'USDCVND':
                    usd_to_vnd = float(ticker['lastPrice'])
            
            if usd_to_vnd is None:
                results.append("Crypto: USD/VND rate not available")
                return results
            
            # Process requested symbols
            for symbol in symbols:
                symbol_upper = symbol.upper()
                
                if symbol_upper in ticker_map:
                    ticker = ticker_map[symbol_upper]
                    usd_price = float(ticker['lastPrice'])
                    vnd_price = usd_price * usd_to_vnd
                    change_24h = float(ticker['priceChangePercent'])
                    
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
                    results.append(f"{symbol}: Not found on Binance")
                
        except Exception as e:
            results.append(f"Crypto: ERROR - {str(e)[:50]}")
        
        return results