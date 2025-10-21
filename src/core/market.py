"""Market data fetching and real-time price monitoring"""
import asyncio
import aiohttp
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class Market:
    """Represents a Polymarket market"""
    id: str
    question: str
    condition_id: str
    yes_token_id: str = ""
    no_token_id: str = ""
    yes_price: float = 0.0
    no_price: float = 0.0
    active: bool = True
    
    def __str__(self):
        return f"{self.question} (YES: ${self.yes_price:.4f}, NO: ${self.no_price:.4f})"


class PolymarketAPI:
    """Real-time Polymarket API integration"""
    
    def __init__(self):
        self.gamma_api = "https://gamma-api.polymarket.com"
        self.clob_api = "https://clob.polymarket.com"
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=10)
            self.session = aiohttp.ClientSession(timeout=timeout)
    
    async def close(self):
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def fetch_markets(self, limit: int = 50) -> List[Market]:
        """Fetch active markets from Polymarket"""
        await self._ensure_session()
        
        try:
            url = f"{self.gamma_api}/markets"
            params = {
                "limit": limit,
                "active": "true",
                "closed": "false",
                "archived": "false"
            }
            
            logger.info(f"Fetching {limit} markets from Polymarket...")
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch markets: HTTP {response.status}")
                    return []
                
                data = await response.json()
                markets = []
                
                for item in data[:limit]:
                    try:
                        # Extract market data
                        market_id = item.get('id', '')
                        condition_id = item.get('condition_id', item.get('conditionId', ''))
                        question = item.get('question', 'Unknown Market')
                        
                        # Get token IDs from outcomes
                        tokens = item.get('tokens', [])
                        yes_token = tokens[0].get('token_id', '') if len(tokens) > 0 else ''
                        no_token = tokens[1].get('token_id', '') if len(tokens) > 1 else ''
                        
                        market = Market(
                            id=market_id,
                            question=question,
                            condition_id=condition_id,
                            yes_token_id=yes_token,
                            no_token_id=no_token,
                            active=item.get('active', True)
                        )
                        markets.append(market)
                    except Exception as e:
                        logger.warning(f"Error parsing market: {e}")
                        continue
                
                logger.info(f"✓ Fetched {len(markets)} markets")
                return markets
                
        except Exception as e:
            logger.error(f"Error fetching markets: {e}")
            return []
    
    async def get_live_prices(self, token_id: str) -> Optional[Dict[str, float]]:
        """Get real-time price for a specific token"""
        await self._ensure_session()
        
        try:
            url = f"{self.clob_api}/price"
            params = {"token_id": token_id}
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    return None
                
                data = await response.json()
                
                # Extract mid price (average of bid/ask)
                mid_price = float(data.get('mid', data.get('price', 0)))
                
                return {
                    'price': mid_price,
                    'bid': float(data.get('bid', mid_price)),
                    'ask': float(data.get('ask', mid_price))
                }
                
        except Exception as e:
            logger.debug(f"Error fetching price for {token_id}: {e}")
            return None
    
    async def get_market_prices(self, market: Market) -> tuple[float, float]:
        """Get current YES and NO prices for a market"""
        
        # Fetch YES price
        yes_data = await self.get_live_prices(market.yes_token_id)
        yes_price = yes_data['price'] if yes_data else 0.50
        
        # Fetch NO price
        no_data = await self.get_live_prices(market.no_token_id)
        no_price = no_data['price'] if no_data else 0.50
        
        return yes_price, no_price
    
    async def get_orderbook(self, token_id: str) -> Optional[Dict]:
        """Get full orderbook for a token"""
        await self._ensure_session()
        
        try:
            url = f"{self.clob_api}/book"
            params = {"token_id": token_id}
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    return None
                
                data = await response.json()
                return {
                    'bids': data.get('bids', []),
                    'asks': data.get('asks', [])
                }
                
        except Exception as e:
            logger.debug(f"Error fetching orderbook: {e}")
            return None
    
    async def place_order(
        self, 
        token_id: str, 
        side: str, 
        amount: float, 
        price: float
    ) -> Dict:
        """
        Simulate order placement (DEMO MODE)
        In production, this would use py-clob-client to place real orders
        """
        logger.info(f"[DEMO] Placing {side.upper()} order:")
        logger.info(f"[DEMO]   Token: {token_id}")
        logger.info(f"[DEMO]   Amount: ${amount:.4f}")
        logger.info(f"[DEMO]   Price: ${price:.4f}")
        
        # Simulate order success
        return {
            'success': True,
            'order_id': f"demo_{token_id[:8]}",
            'side': side,
            'amount': amount,
            'price': price,
            'status': 'filled'
        }
    
    async def execute_arbitrage_trade(
        self,
        market: Market,
        yes_price: float,
        no_price: float,
        amount: float = 1.0
    ) -> Dict:
        """
        Execute arbitrage trade (DEMO MODE)
        Buys YES and NO shares, simulates merge
        """
        logger.info(f"[DEMO] Executing arbitrage on: {market.question}")
        
        # Buy YES share
        yes_order = await self.place_order(
            market.yes_token_id,
            'buy',
            amount,
            yes_price
        )
        
        # Buy NO share
        no_order = await self.place_order(
            market.no_token_id,
            'buy',
            amount,
            no_price
        )
        
        # Simulate merge (in real mode, this would be a blockchain transaction)
        logger.info(f"[DEMO] Merging YES + NO positions...")
        logger.info(f"[DEMO] Received: ${amount:.4f}")
        
        return {
            'yes_order': yes_order,
            'no_order': no_order,
            'merge_amount': amount,
            'total_cost': yes_price + no_price,
            'profit': amount - (yes_price + no_price)
        }
