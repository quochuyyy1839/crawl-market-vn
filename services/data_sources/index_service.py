"""
VN-Index service
"""
from vnstock import Vnstock
from ..core.base_service import BaseMarketDataService

class IndexService(BaseMarketDataService):
    """Service for fetching VN-Index data"""
    
    def __init__(self):
        super().__init__("VN-Index")
    
    def fetch_data(self) -> str:
        """Get VN-Index with daily changes"""
        try:
            from datetime import datetime, timedelta
            
            # Dynamic date range - last 30 days to today
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            index_obj = Vnstock().world_index(symbol='VNI', source='MSN')
            data = index_obj.quote.history(start=start_date, end=end_date, interval='1D')
            
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