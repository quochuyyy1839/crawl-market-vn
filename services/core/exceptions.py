"""
Custom exceptions for market data services
"""

class MarketDataError(Exception):
    """Base exception for market data errors"""
    pass

class DataFetchError(MarketDataError):
    """Exception raised when data fetching fails"""
    
    def __init__(self, source: str, message: str, original_error: Exception = None):
        self.source = source
        self.message = message
        self.original_error = original_error
        super().__init__(f"{source}: {message}")

class DataParsingError(MarketDataError):
    """Exception raised when data parsing fails"""
    
    def __init__(self, source: str, message: str):
        self.source = source
        self.message = message
        super().__init__(f"{source}: Failed to parse data - {message}")

class APIError(MarketDataError):
    """Exception raised for API-related errors"""
    
    def __init__(self, source: str, status_code: int, message: str):
        self.source = source
        self.status_code = status_code
        self.message = message
        super().__init__(f"{source}: API error {status_code} - {message}")