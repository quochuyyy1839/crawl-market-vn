"""
VCB exchange rate service
"""
from typing import List
from datetime import datetime
from vnstock.explorer.misc import vcb_exchange_rate
from ..core.base_service import BaseMarketDataService

class ExchangeService(BaseMarketDataService):
    """Service for fetching VCB exchange rates"""
    
    def __init__(self):
        super().__init__("VCB Exchange")
    
    def fetch_data(self, currencies: List[str]) -> List[str]:
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
                            buy_clean = str(buy).replace(',', '') if buy != 'N/A' else '0'
                            buy_num = float(buy_clean)
                            buy_formatted = f"{buy_num/1000:,.1f}k VND" if buy_num > 0 else str(buy)
                        except (ValueError, TypeError):
                            buy_formatted = str(buy)
                        
                        try:
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