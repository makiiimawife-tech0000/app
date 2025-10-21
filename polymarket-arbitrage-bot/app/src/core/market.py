"""Market data fetching and real-time price monitoring"""
import asyncio
import aiohttp
import json
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
                "limit": min(limit * 3, 150),  # Fetch more to account for filtering
                "active": "true",
                "closed": "false",
                "archived": "false"
            }
            
            logger.info(f"Fetching markets from Polymarket...")
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch markets: HTTP {response.status}")
                    return []
                
                data = await response.json()
                markets = []
                processed = 0
                
                # Process markets to get detailed info with token IDs
                for item in data:
                    if len(markets) >= limit:
                        break
                        
                    try:
                        market_id = item.get('id', '')
                        question = item.get('question', 'Unknown Market')
                        processed += 1
                        
                        # Skip if essential data is missing
                        if not market_id or not question:
                            continue
                        
                        # Skip inactive or closed markets
                        if not item.get('active', True) or item.get('closed', False):
                            continue
                        
                        # Get detailed market info to fetch token IDs
                        detail_url = f"{self.gamma_api}/markets/{market_id}"
                        try:
                            async with self.session.get(detail_url) as detail_response:
                                if detail_response.status != 200:
                                    continue
                                
                                detail = await detail_response.json()
                                
                                # Extract token IDs from clobTokenIds
                                clob_token_ids = detail.get('clobTokenIds', [])
                                if not clob_token_ids or len(clob_token_ids) < 2:
                                    continue
                                
                                # Parse outcomes to determine which token is YES/NO
                                outcomes_raw = detail.get('outcomes', [])
                                if isinstance(outcomes_raw, str):
                                    try:
                                        outcomes = json.loads(outcomes_raw)
                                    except json.JSONDecodeError:
                                        outcomes = ['Yes', 'No']  # Default fallback
                                else:
                                    outcomes = outcomes_raw
                                
                                # Map tokens to YES/NO based on outcomes
                                yes_token = clob_token_ids[0]  # Default: first is YES
                                no_token = clob_token_ids[1]   # Default: second is NO
                                
                                # Try to be smarter about token mapping
                                if len(outcomes) >= 2:
                                    for i, outcome in enumerate(outcomes[:2]):
                                        outcome_text = str(outcome).lower()
                                        if i < len(clob_token_ids):
                                            if 'yes' in outcome_text:
                                                yes_token = clob_token_ids[i]
                                            elif 'no' in outcome_text:
                                                no_token = clob_token_ids[i]
                                
                                market = Market(
                                    id=market_id,
                                    question=question,
                                    condition_id=detail.get('conditionId', ''),
                                    yes_token_id=yes_token,
                                    no_token_id=no_token,
                                    active=detail.get('active', True)
                                )
                                markets.append(market)
                                
                        except Exception as e:
                            logger.debug(f"Error fetching details for market {market_id}: {e}")
                            continue
                            
                    except Exception as e:
                        logger.debug(f"Error processing market: {e}")
                        continue
                
                logger.info(f"✓ Fetched {len(markets)} markets with token IDs (processed {processed})")
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
                    logger.debug(f"Price API returned status {response.status} for token {token_id}")
                    return None
                
                data = await response.json()
                
                # Extract mid price (average of bid/ask)
                mid_price = float(data.get('mid', data.get('price', 0)))
                
                # Validate price is reasonable (between 0 and 1)
                if not (0 <= mid_price <= 1):
                    logger.warning(f"Invalid price {mid_price} for token {token_id}")
                    return None
                
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
        
        # Validate token IDs
        if not market.yes_token_id or not market.no_token_id:
            logger.warning(f"Missing token IDs for market {market.id}")
            return 0.50, 0.50
        
        # Fetch YES price
        yes_data = await self.get_live_prices(market.yes_token_id)
        yes_price = yes_data['price'] if yes_data else 0.50
        
        # Fetch NO price  
        no_data = await self.get_live_prices(market.no_token_id)
        no_price = no_data['price'] if no_data else 0.50
        
        # Ensure prices are reasonable
        yes_price = max(0.01, min(0.99, yes_price))
        no_price = max(0.01, min(0.99, no_price))
        
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
