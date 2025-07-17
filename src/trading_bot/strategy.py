from datetime import datetime, timezone  # Import datetime for timestamps
from .data_fetcher import DataFetcher  # Import our data fetcher

# Define the Strategy class, which will contain your trading logic
class ArbitrageStrategy:
    def __init__(self, min_spread_pct: float = 0.5):
        """
        Initialize the arbitrage strategy.
        Args:
            min_spread_pct: Minimum spread percentage to trigger a trade (default 0.5%)
        """
        self.data_fetcher = DataFetcher()  # Create data fetcher instance
        self.min_spread_pct = min_spread_pct  # Minimum spread to trade
        self.last_trade_time = None  # Track last trade to avoid spam
        
    def on_tick(self, data):
        """
        This method is called on every new tick (row of data).
        For arbitrage, we'll fetch live prices and check for opportunities.
        Args:
            data: Dictionary with tick data (e.g., price, timestamp, etc.)
        Returns:
            A signal dictionary (e.g., {"side": "buy", "qty": 1}) or None for no action
        """
        # Get current prices from both exchanges
        binance_price, kraken_price = self.data_fetcher.get_both_prices()
        
        # If we can't get prices from both exchanges, skip this tick
        if not binance_price or not kraken_price:
            print("⚠️  Could not fetch prices from both exchanges")
            return None
        
        # Calculate the spread between exchanges
        spread_info = self.data_fetcher.calculate_spread(binance_price, kraken_price)
        
        # Check if spread is large enough to be profitable (after fees)
        spread_pct = spread_info["spread_pct"]
        if isinstance(spread_pct, float) and spread_pct >= self.min_spread_pct:
            print(f"🎯 Arbitrage opportunity found!")
            print(f"   Spread: {spread_info['spread_pct']:.3f}%")
            print(f"   Buy on: {spread_info['lower_exchange']} at ${spread_info['lower_price']:,.2f}")
            print(f"   Sell on: {spread_info['higher_exchange']} at ${spread_info['higher_price']:,.2f}")
            
            # Return arbitrage signal
            return {
                "side": "arbitrage",
                "buy_exchange": spread_info["lower_exchange"],
                "sell_exchange": spread_info["higher_exchange"],
                "buy_price": spread_info["lower_price"],
                "sell_price": spread_info["higher_price"],
                "spread_pct": spread_info["spread_pct"],
                "qty": 1  # Trade 1 BTC
            }
        
        # No profitable opportunity found
        return None

# Keep the old Strategy class for backward compatibility
class Strategy:
    def on_tick(self, data):
        """
        This method is called on every new tick (row of data).
        Args:
            data: Dictionary with tick data (e.g., price, timestamp, etc.)
        Returns:
            A signal dictionary (e.g., {"side": "buy", "qty": 1}) or None for no action
        """
        # Example logic: if the price is even, return a buy signal
        if data["price"] % 2 == 0:
            return {"side": "buy", "qty": 1}  # Buy 1 unit
        # Otherwise, do nothing (no trade)
        return None

# If you run this file directly, it will run an example tick
if __name__ == "__main__":
    strat = Strategy()  # Create a strategy instance
    # Print the result of running on_tick with price 42
    print(f"{datetime.now(timezone.utc)} | Example tick ->", strat.on_tick({"price": 42}))