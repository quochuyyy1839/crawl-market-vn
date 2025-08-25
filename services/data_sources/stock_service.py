"""
Vietnamese stock price service
"""
from typing import List
from vnstock import Vnstock
from ..core.base_service import BaseMarketDataService

class StockService(BaseMarketDataService):
    """Service for fetching Vietnamese stock prices"""
    
    def __init__(self):
        super().__init__("Vietnamese Stocks")
    
    def fetch_data(self, symbols: List[str]) -> List[str]:
        """Get Vietnamese stock prices with full precision"""
        results = []
        
        for symbol in symbols:
            try:
                stock = Vnstock().stock(symbol=symbol, source='VCI')
                data = stock.quote.history(start='2024-01-01', end='2024-12-31', interval='1D')
                
                if data is not None and len(data) > 0:
                    price = data.iloc[-1]['close']
                    price_formatted = f"{price:,.1f}k VND"
                    results.append(f"{symbol}: {price_formatted}")
                else:
                    results.append(f"{symbol}: N/A")
                    
            except Exception as e:
                error_msg = self.handle_error(e, f"fetching {symbol}")
                results.append(f"{symbol}: ERROR - {str(e)[:30]}")
        
        return results