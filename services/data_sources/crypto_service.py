"""
Cryptocurrency price service
"""
from typing import List
import requests
from ..core.base_service import BaseMarketDataService

class CryptoService(BaseMarketDataService):
    """Service for fetching cryptocurrency prices"""
    
    def __init__(self):
        super().__init__("Cryptocurrency")
    
    def fetch_data(self, symbols: List[str]) -> List[str]:
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