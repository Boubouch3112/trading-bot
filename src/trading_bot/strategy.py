from datetime import datetime, timezone  # Import datetime for timestamps

# Define the Strategy class, which will contain your trading logic
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