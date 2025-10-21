"""Configuration loader"""
import yaml
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv
import os


class Config:
    """Application configuration"""
    
    def __init__(self, config_path: str = "config.yaml"):
        # Handle relative paths by making them relative to the app directory
        if not os.path.isabs(config_path):
            # Get the directory where this file is located
            current_dir = Path(__file__).parent.parent.parent
            self.config_path = current_dir / config_path
        else:
            self.config_path = Path(config_path)
        
        self._config: Dict[str, Any] = {}
        self.load()
        
        # Load environment variables
        load_dotenv()
    
    def load(self):
        """Load configuration from YAML file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        else:
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    @property
    def polymarket_api_url(self) -> str:
        return self.get('polymarket.api_url')
    
    @property
    def polymarket_ws_url(self) -> str:
        return self.get('polymarket.ws_url')
    
    @property
    def gamma_api_url(self) -> str:
        return self.get('polymarket.gamma_api')
    
    @property
    def min_profit(self) -> float:
        return self.get('trading.min_profit_threshold', 0.01)
    
    @property
    def trading_fee(self) -> float:
        return self.get('trading.trading_fee', 0.02)
    
    @property
    def gas_estimate(self) -> float:
        return self.get('trading.gas_estimate', 0.01)
    
    @property
    def demo_balance(self) -> float:
        return self.get('demo.initial_balance', 1000.0)
    
    @property
    def auto_execute(self) -> bool:
        return self.get('ui.auto_execute', True)
    
    # Real mode credentials from environment
    @property
    def api_key(self) -> str:
        return os.getenv('POLYMARKET_API_KEY', '')
    
    @property
    def api_secret(self) -> str:
        return os.getenv('POLYMARKET_SECRET', '')
    
    @property
    def private_key(self) -> str:
        return os.getenv('POLYMARKET_PRIVATE_KEY', '')
    
    @property
    def wallet_address(self) -> str:
        return os.getenv('POLYMARKET_WALLET_ADDRESS', '')


# Global config instance
config = Config()
