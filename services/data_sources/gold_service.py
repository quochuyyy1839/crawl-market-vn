"""
SJC gold price service
"""
from vnstock.explorer.misc import sjc_gold_price
from ..core.base_service import BaseMarketDataService

class GoldService(BaseMarketDataService):
    """Service for fetching SJC gold prices"""
    
    def __init__(self):
        super().__init__("SJC Gold")
    
    def fetch_data(self) -> str:
        """Get SJC gold prices with retry mechanism"""
        import time
        
        for attempt in range(3):  # 3 attempts
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
                if attempt < 2:  # Not last attempt
                    time.sleep(5)  # Wait 5 seconds before retry
                    continue
                else:
                    return f"SJC Gold: Connection failed after 3 attempts - {str(e)[:50]}"