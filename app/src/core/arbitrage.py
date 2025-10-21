"""Arbitrage detection logic"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ArbitrageOpportunity:
    """Represents an arbitrage opportunity"""
    market_id: str
    market_name: str
    yes_price: float
    no_price: float
    total_cost: float
    estimated_profit: float
    profit_percentage: float


class ArbitrageDetector:
    """Detects arbitrage opportunities"""
    
    def __init__(self, min_profit: float = 0.01, trading_fee: float = 0.02, gas_cost: float = 0.01):
        """
        Args:
            min_profit: Minimum profit threshold in USD
            trading_fee: Trading fee percentage (e.g., 0.02 for 2%)
            gas_cost: Estimated gas cost in USD
        """
        self.min_profit = min_profit
        self.trading_fee = trading_fee
        self.gas_cost = gas_cost
    
    def check_arbitrage(
        self, 
        market_id: str,
        market_name: str,
        yes_price: float, 
        no_price: float
    ) -> Optional[ArbitrageOpportunity]:
        """
        Check if there's an arbitrage opportunity
        
        Args:
            market_id: Unique market identifier
            market_name: Human-readable market name
            yes_price: Price of YES share
            no_price: Price of NO share
            
        Returns:
            ArbitrageOpportunity if profitable, None otherwise
        """
        # Calculate total cost
        total_share_cost = yes_price + no_price
        
        # Calculate fees
        fee_amount = total_share_cost * self.trading_fee
        
        # Total cost including fees and gas
        total_cost = total_share_cost + fee_amount + self.gas_cost
        
        # Revenue from merging (always $1.00)
        revenue = 1.0
        
        # Calculate profit
        profit = revenue - total_cost
        
        # Check if profitable
        if profit > self.min_profit:
            profit_percentage = (profit / total_cost) * 100
            
            return ArbitrageOpportunity(
                market_id=market_id,
                market_name=market_name,
                yes_price=yes_price,
                no_price=no_price,
                total_cost=total_cost,
                estimated_profit=profit,
                profit_percentage=profit_percentage
            )
        
        return None
    
    def calculate_profit(self, yes_price: float, no_price: float) -> float:
        """Calculate profit for given prices"""
        total_cost = yes_price + no_price
        fee = total_cost * self.trading_fee
        return 1.0 - total_cost - fee - self.gas_cost
