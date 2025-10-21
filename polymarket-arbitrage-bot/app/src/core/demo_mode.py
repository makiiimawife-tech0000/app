"""Demo mode - simulated trading with fake money"""
from typing import List
from dataclasses import dataclass
from datetime import datetime
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class DemoTrade:
    """Represents a demo trade"""
    timestamp: datetime
    market_name: str
    yes_price: float
    no_price: float
    total_cost: float
    profit: float
    
    def __str__(self):
        return (f"[DEMO] {self.timestamp.strftime('%H:%M:%S')} - {self.market_name}: "
                f"YES ${self.yes_price:.2f} + NO ${self.no_price:.2f} = "
                f"${self.total_cost:.2f} → Profit: ${self.profit:.4f}")


class DemoMode:
    """Demo trading mode with simulated money"""
    
    def __init__(self, initial_balance: float = 1000.0):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.total_profit = 0.0
        self.trades: List[DemoTrade] = []
        self.num_trades = 0
    
    def execute_arbitrage(
        self,
        market_name: str,
        yes_price: float,
        no_price: float,
        trading_fee: float = 0.02,
        gas_cost: float = 0.01
    ) -> DemoTrade:
        """
        Execute a simulated arbitrage trade
        
        Args:
            market_name: Name of the market
            yes_price: YES share price
            no_price: NO share price
            trading_fee: Trading fee percentage
            gas_cost: Estimated gas cost
            
        Returns:
            DemoTrade object with results
        """
        # Calculate costs
        share_cost = yes_price + no_price
        fee_amount = share_cost * trading_fee
        total_cost = share_cost + fee_amount + gas_cost
        
        # Simulate buying
        logger.info(f"[DEMO] Buying YES share @ ${yes_price:.2f}")
        logger.info(f"[DEMO] Buying NO share @ ${no_price:.2f}")
        
        # Update balance
        self.balance -= total_cost
        
        # Simulate merging (always receive $1.00)
        logger.info(f"[DEMO] Merging positions...")
        merge_payout = 1.0
        self.balance += merge_payout
        
        # Calculate profit
        profit = merge_payout - total_cost
        self.total_profit += profit
        self.num_trades += 1
        
        # Create trade record
        trade = DemoTrade(
            timestamp=datetime.now(),
            market_name=market_name,
            yes_price=yes_price,
            no_price=no_price,
            total_cost=total_cost,
            profit=profit
        )
        
        self.trades.append(trade)
        
        logger.info(f"[DEMO] Trade complete! Profit: ${profit:.4f}")
        logger.info(f"[DEMO] New balance: ${self.balance:.2f}")
        
        return trade
    
    def get_stats(self) -> dict:
        """Get trading statistics"""
        avg_profit = self.total_profit / self.num_trades if self.num_trades > 0 else 0
        
        return {
            'initial_balance': self.initial_balance,
            'current_balance': self.balance,
            'total_profit': self.total_profit,
            'num_trades': self.num_trades,
            'avg_profit': avg_profit,
            'win_rate': 100.0 if self.num_trades > 0 else 0  # Arbitrage always wins
        }
    
    def reset(self):
        """Reset demo account to initial state"""
        self.balance = self.initial_balance
        self.total_profit = 0.0
        self.trades = []
        self.num_trades = 0
        logger.info(f"[DEMO] Account reset to ${self.initial_balance:.2f}")
