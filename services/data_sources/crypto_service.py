"""
Cryptocurrency price service using CryptoCompare API
"""
from typing import List
import requests
from datetime import datetime
from vnstock.explorer.misc import vcb_exchange_rate
from ..core.base_service import BaseMarketDataService

class CryptoService(BaseMarketDataService):
    """Service for fetching cryptocurrency prices from CryptoCompare API"""
    
    def __init__(self):
        super().__init__("Cryptocurrency")
    
    def _get_usd_vnd_rate(self):
        """Get USD/VND rate from VCB exchange service. Returns None if unavailable."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            rate_data = vcb_exchange_rate(date=today)
            
            if rate_data is not None and len(rate_data) > 0:
                usd_row = rate_data[rate_data['currency_code'] == 'USD']
                
                if len(usd_row) > 0:
                    row = usd_row.iloc[0]
                    # Use sell rate (what you pay in VND to buy USD)
                    sell_rate = row.get('sell', 'N/A')
                    
                    if sell_rate != 'N/A':
                        # Clean and convert to float
                        sell_clean = str(sell_rate).replace(',', '')
                        return float(sell_clean)
        except Exception:
            pass
        
        return None
    
    def fetch_data(self, symbols: List[str]) -> List[str]:
        """Get cryptocurrency prices from CryptoCompare API with VCB USD/VND rate"""
        results = []
        
        try:
            # Get real USD to VND rate from VCB
            usd_to_vnd = self._get_usd_vnd_rate()
            
            # Get prices for all symbols in one request
            symbols_str = ','.join(symbols)
            url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={symbols_str}&tsyms=USD"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                results.append(f"Crypto: CryptoCompare API error {response.status_code}")
                return results
            
            data = response.json()
            
            if 'RAW' not in data:
                results.append("Crypto: No data available")
                return results
            
            # Process each symbol from .env
            for symbol in symbols:
                if symbol in data['RAW']:
                    crypto_data = data['RAW'][symbol]['USD']
                    
                    usd_price = float(crypto_data['PRICE'])
                    change_24h = float(crypto_data['CHANGEPCT24HOUR'])
                    
                    change_sign = "+" if change_24h >= 0 else ""
                    
                    # Format output based on whether VCB rate is available
                    if usd_to_vnd is not None:
                        vnd_price = usd_price * usd_to_vnd
                        
                        # Format VND price
                        if vnd_price > 1000000:
                            vnd_formatted = f"{vnd_price/1000000:,.1f}M VND"
                        elif vnd_price > 1000:
                            vnd_formatted = f"{vnd_price/1000:,.0f}k VND"
                        else:
                            vnd_formatted = f"{vnd_price:,.0f} VND"
                        
                        results.append(f"{symbol}: ${usd_price:,.2f} / {vnd_formatted} ({change_sign}{change_24h:.2f}%)")
                    else:
                        # VCB rate unavailable, show only USD
                        results.append(f"{symbol}: ${usd_price:,.2f} ({change_sign}{change_24h:.2f}%)")
                else:
                    results.append(f"{symbol}: Not available")
                
        except Exception as e:
            results.append(f"Crypto: ERROR - {str(e)[:50]}")
        
        return results