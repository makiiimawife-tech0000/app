"""Market data fetching and monitoring"""
import asyncio
import aiohttp
import json
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
import websockets
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class Market:
    """Represents a Polymarket market"""
    id: str
    question: str
    yes_price: float = 0.0
    no_price: float = 0.0
    active: bool = True
    end_date: Optional[str] = None
    
    def __str__(self):
        return f"{self.question} (YES: ${self.yes_price:.2f}, NO: ${self.no_price:.2f})"


class MarketDataFetcher:
    """Fetches market data from Polymarket API"""
    
    def __init__(self, api_url: str = "https://gamma-api.polymarket.com", clob_url: str = "https://clob.polymarket.com"):
        self.api_url = api_url
        self.clob_url = clob_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
    
    async def close(self):
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def fetch_markets(self, limit: int = 100) -> List[Market]:
        """
        Fetch active markets from Polymarket
        
        Args:
            limit: Maximum number of markets to fetch
            
        Returns:
            List of Market objects
        """
        await self._ensure_session()
        
        try:
            # Fetch from Gamma API (simpler structure)
            url = f"{self.api_url}/markets"
            params = {
                "limit": limit,
                "active": "true",
                "closed": "false"
            }
            
            logger.info(f"Fetching markets from {url}")
            
            async with self.session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    markets = []
                    
                    # Parse markets
                    for item in data[:limit]:
                        try:
                            market = Market(
                                id=item.get('id', item.get('condition_id', '')),
                                question=item.get('question', 'Unknown Market'),
                                active=item.get('active', True),
                                end_date=item.get('end_date_iso')
                            )
                            markets.append(market)
                        except Exception as e:
                            logger.warning(f"Error parsing market: {e}")
                            continue
                    
                    logger.info(f"Fetched {len(markets)} markets")
                    return markets
                else:
                    logger.error(f"Failed to fetch markets: HTTP {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error fetching markets: {e}")
            return []
    
    async def get_market_prices(self, market_id: str) -> Optional[Dict[str, float]]:
        """
        Get current prices for a specific market
        
        Args:
            market_id: Market identifier
            
        Returns:
            Dict with 'yes' and 'no' prices, or None
        """
        await self._ensure_session()
        
        try:
            # Try CLOB API for price data
            url = f"{self.clob_url}/prices"
            params = {"market": market_id}
            
            async with self.session.get(url, params=params, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Parse prices (structure varies)
                    if isinstance(data, dict):
                        yes_price = float(data.get('yes', data.get('YES', 0.5)))
                        no_price = float(data.get('no', data.get('NO', 0.5)))
                        
                        return {
                            'yes': yes_price,
                            'no': no_price
                        }
        except Exception as e:
            logger.warning(f"Error fetching prices for {market_id}: {e}")
        
        # Return default prices if fetch fails
        return {'yes': 0.5, 'no': 0.5}
    
    async def search_markets(self, query: str, markets: List[Market]) -> List[Market]:
        """
        Search markets by query string
        
        Args:
            query: Search string
            markets: List of markets to search
            
        Returns:
            Filtered list of markets
        """
        query_lower = query.lower()
        return [m for m in markets if query_lower in m.question.lower()]


class MarketMonitor:
    """Monitors market prices in real-time"""
    
    def __init__(self, ws_url: str = "wss://ws-subscriptions-clob.polymarket.com/ws/market"):
        self.ws_url = ws_url
        self.running = False
        self.websocket = None
        self.price_callback: Optional[Callable] = None
    
    async def connect(self, market_id: str, callback: Callable[[float, float], None]):
        """
        Connect to WebSocket and monitor prices
        
        Args:
            market_id: Market to monitor
            callback: Function called with (yes_price, no_price) on updates
        """
        self.price_callback = callback
        self.running = True
        
        try:
            # For now, simulate price updates since WebSocket structure may vary
            # In production, you'd connect to actual Polymarket WebSocket
            logger.info(f"Starting price monitoring for market {market_id}")
            
            while self.running:
                # Simulate price updates (replace with actual WebSocket in production)
                # This is a placeholder for demo mode
                await asyncio.sleep(0.5)  # Update every 500ms
                
                # In real implementation, parse WebSocket messages here
                # For now, this will be driven by manual price updates
                
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            await self.disconnect()
    
    async def disconnect(self):
        """Disconnect from WebSocket"""
        self.running = False
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
        logger.info("Disconnected from price feed")
    
    def update_prices(self, yes_price: float, no_price: float):
        """Manual price update (for testing/demo)"""
        if self.price_callback and self.running:
            self.price_callback(yes_price, no_price)
