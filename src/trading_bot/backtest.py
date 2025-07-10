import pandas as pd  # Import pandas for data manipulation
from datetime import datetime, timezone  # Import datetime for timestamps
from typing import Dict, List, Optional, Any  # Import typing for type hints
from .strategy import Strategy  # Import the Strategy class from the same package

# Define the Backtest class, which will handle running the backtest simulation
class Backtest:
    def __init__(self, initial_capital: float = 10000):
        # Set the initial amount of money to start with
        self.initial_capital = initial_capital
        # Set the current available cash (starts as initial_capital)
        self.capital = initial_capital
        # Set the number of positions (units of asset held)
        self.positions = 0
        # List to store all executed trades
        self.trades = []
        # List to store the equity (account value) over time
        self.equity_curve = []
        
    def run(self, data: pd.DataFrame, strategy: Strategy) -> Dict[str, Any]:
        """
        Run the backtest on historical data using the provided strategy.
        Args:
            data: DataFrame with columns ['timestamp', 'price', ...]
            strategy: Strategy instance to test
        Returns:
            Dictionary with backtest results and statistics
        """
        # Reset all state for a new run
        self.capital = self.initial_capital
        self.positions = 0
        self.trades = []
        self.equity_curve = []
        
        # Iterate over each row (tick) in the data
        for index, row in data.iterrows():
            # Prepare the tick data for the strategy (price, timestamp, and any other columns)
            tick_data = {
                "price": row["price"],  # Current price
                "timestamp": row["timestamp"],  # Current timestamp
                **row.to_dict()  # Include all other columns (e.g., volume)
            }
            
            # Get the trading signal from the strategy (e.g., {"side": "buy", "qty": 1})
            signal = strategy.on_tick(tick_data)
            
            # If the strategy returns a signal, execute it
            if signal:
                self._execute_signal(signal, tick_data)
            
            # Calculate the current equity (cash + value of held positions)
            current_equity = self.capital + (self.positions * tick_data["price"])
            # Record the equity, price, and positions at this tick
            self.equity_curve.append({
                "timestamp": tick_data["timestamp"],
                "equity": current_equity,
                "price": tick_data["price"],
                "positions": self.positions
            })
        
        # After all ticks, calculate and return the results
        return self._calculate_results()
    
    def _execute_signal(self, signal: Dict[str, Any], tick_data: Dict[str, Any]):
        """
        Execute a trading signal (buy or sell) from the strategy.
        Args:
            signal: Dictionary with trade info (e.g., {"side": "buy", "qty": 1})
            tick_data: Dictionary with current tick info
        """
        side = signal.get("side")  # 'buy' or 'sell'
        qty = signal.get("qty", 1)  # Quantity to trade (default 1)
        price = tick_data["price"]  # Current price
        
        # If the signal is to buy and we have enough cash
        if side == "buy" and self.capital >= price * qty:
            cost = price * qty  # Total cost of the buy
            self.capital -= cost  # Subtract cost from cash
            self.positions += qty  # Add to positions
            # Record the trade
            self.trades.append({
                "timestamp": tick_data["timestamp"],
                "side": "buy",
                "price": price,
                "qty": qty,
                "cost": cost
            })
        # If the signal is to sell and we have enough positions
        elif side == "sell" and self.positions >= qty:
            revenue = price * qty  # Total revenue from the sell
            self.capital += revenue  # Add revenue to cash
            self.positions -= qty  # Subtract from positions
            # Record the trade
            self.trades.append({
                "timestamp": tick_data["timestamp"],
                "side": "sell",
                "price": price,
                "qty": qty,
                "revenue": revenue
            })
    
    def _calculate_results(self) -> Dict[str, Any]:
        """
        Calculate statistics and results for the backtest.
        Returns:
            Dictionary with performance metrics and trade history
        """
        # If no data was processed, return an error
        if not self.equity_curve:
            return {"error": "No data processed"}
        
        initial_equity = self.initial_capital  # Starting equity
        final_equity = self.equity_curve[-1]["equity"]  # Ending equity
        total_return = (final_equity - initial_equity) / initial_equity * 100  # % return
        
        # Calculate max drawdown (largest drop from a peak)
        peak = initial_equity  # Highest equity seen so far
        max_drawdown = 0  # Largest drawdown seen so far
        for point in self.equity_curve:
            if point["equity"] > peak:
                peak = point["equity"]  # Update peak
            drawdown = (peak - point["equity"]) / peak * 100  # % drop from peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown  # Update max drawdown
        
        # Return all results as a dictionary
        return {
            "initial_capital": initial_equity,
            "final_equity": final_equity,
            "total_return_pct": total_return,
            "total_trades": len(self.trades),
            "max_drawdown_pct": max_drawdown,
            "trades": self.trades,
            "equity_curve": self.equity_curve
        }

# Function to create sample price data for testing the backtest
# You can replace this with your own data loader

def create_sample_data(start_date: str = "2024-01-01", days: int = 30) -> pd.DataFrame:
    import numpy as np  # Import numpy for random number generation
    dates = pd.date_range(start=start_date, periods=days, freq='D')  # Create a range of dates
    np.random.seed(42)  # Set random seed for reproducibility
    base_price = 100.0  # Start price as a float
    prices = [base_price]  # List of prices, starting with base_price
    for i in range(1, days):
        change = np.random.normal(0.5, 2)  # Simulate a daily price change (mean=0.5, std=2)
        new_price = prices[-1] + change  # Add change to last price
        prices.append(max(new_price, 1))  # Prevent negative prices
    # Return a DataFrame with timestamp, price, and random volume
    return pd.DataFrame({
        "timestamp": dates,
        "price": prices,
        "volume": np.random.randint(1000, 10000, days)
    })

# If you run this file directly, it will run a sample backtest
if __name__ == "__main__":
    from strategy import Strategy  # Import your strategy
    data = create_sample_data()  # Generate sample data
    print("Sample data:")
    print(data.head())  # Show first few rows
    print("\n" + "="*50 + "\n")
    strategy = Strategy()  # Create a strategy instance
    backtest = Backtest(initial_capital=10000)  # Create a backtest instance
    results = backtest.run(data, strategy)  # Run the backtest
    print("Backtest Results:")
    print(f"Initial Capital: ${results['initial_capital']:,.2f}")  # Show starting capital
    print(f"Final Equity: ${results['final_equity']:,.2f}")  # Show ending equity
    print(f"Total Return: {results['total_return_pct']:.2f}%")  # Show % return
    print(f"Total Trades: {results['total_trades']}")  # Show number of trades
    print(f"Max Drawdown: {results['max_drawdown_pct']:.2f}%")  # Show max drawdown
    if results['trades']:
        print(f"\nFirst few trades:")
        for trade in results['trades'][:5]:
            print(f"  {trade['timestamp'].date()} | {trade['side'].upper()} | "
                  f"Price: ${trade['price']:.2f} | Qty: {trade['qty']}") 