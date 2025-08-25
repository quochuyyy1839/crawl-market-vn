"""
Abstract base class for market data services
"""
from abc import ABC, abstractmethod
from typing import Any, List, Optional
from .exceptions import DataFetchError

class BaseMarketDataService(ABC):
    """Abstract base class for all market data services"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
    
    @abstractmethod
    def fetch_data(self, *args, **kwargs) -> Any:
        """Fetch data from the source. Must be implemented by subclasses."""
        pass
    
    def handle_error(self, error: Exception, context: str = "") -> str:
        """Handle errors in a consistent way across all services"""
        error_msg = f"{self.service_name}: ERROR"
        
        if context:
            error_msg += f" ({context})"
        
        # Truncate long error messages
        error_detail = str(error)[:50]
        error_msg += f" - {error_detail}"
        
        return error_msg
    
    def safe_fetch(self, fetch_func, *args, **kwargs) -> Any:
        """Safely execute a fetch function with error handling"""
        try:
            return fetch_func(*args, **kwargs)
        except Exception as e:
            error_msg = self.handle_error(e, "fetch failed")
            print(f"[{self.service_name}] {error_msg}")
            raise DataFetchError(self.service_name, str(e), e)