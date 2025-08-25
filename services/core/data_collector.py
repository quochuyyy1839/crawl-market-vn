"""
Data collector that orchestrates fetching data from all sources
"""
from typing import Dict, Any, Optional, List
from .exceptions import DataFetchError

class DataCollector:
    """Orchestrates data collection from multiple sources"""
    
    def __init__(self):
        self.services = {}
        self.results = {}
    
    def register_service(self, name: str, service, enabled: bool = True):
        """Register a data service"""
        self.services[name] = {
            'service': service,
            'enabled': enabled
        }
    
    def collect_all(self, service_configs: Dict[str, Any]) -> Dict[str, Any]:
        """Collect data from all enabled services"""
        results = {}
        
        for name, config in self.services.items():
            if not config['enabled']:
                continue
                
            service = config['service']
            service_config = service_configs.get(name, {})
            
            try:
                print(f"Fetching data from {service.service_name}...")
                data = service.fetch_data(**service_config)
                results[name] = data
            except DataFetchError as e:
                print(f"Failed to fetch from {service.service_name}: {e}")
                results[name] = None
            except Exception as e:
                print(f"Unexpected error from {service.service_name}: {e}")
                results[name] = None
        
        return results
    
    def get_service_names(self) -> List[str]:
        """Get list of all registered service names"""
        return list(self.services.keys())
    
    def enable_service(self, name: str):
        """Enable a specific service"""
        if name in self.services:
            self.services[name]['enabled'] = True
    
    def disable_service(self, name: str):
        """Disable a specific service"""
        if name in self.services:
            self.services[name]['enabled'] = False