"""
Common HTTP client with retry logic
"""
import requests
from time import sleep
from typing import Optional, Dict, Any

class APIClient:
    """HTTP client with retry logic and common headers"""
    
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MarketBot/1.0)'}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """GET request with retry logic"""
        return self._request('GET', url, params=params, headers=headers)
    
    def post(self, url: str, data: Optional[Dict] = None, json: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """POST request with retry logic"""
        return self._request('POST', url, data=data, json=json, headers=headers)
    
    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Execute request with retry logic"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                return response
                
            except requests.exceptions.RequestException as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Request failed (attempt {attempt + 1}/{self.max_retries + 1}), retrying in {wait_time}s...")
                    sleep(wait_time)
                else:
                    print(f"Request failed after {self.max_retries + 1} attempts")
        
        raise last_exception
    
    def close(self):
        """Close the session"""
        self.session.close()

# Global instance for convenient access
http_client = APIClient()