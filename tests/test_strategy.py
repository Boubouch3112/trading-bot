import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from trading_bot.strategy import Strategy

class TestStrategy:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.strategy = Strategy()

    def test_buy_signal_for_even_price(self):
        """Test that strategy returns buy signal for even prices."""
        result = self.strategy.on_tick({"price": 42})
        assert result == {"side": "buy", "qty": 1}

    def test_no_signal_for_odd_price(self):
        """Test that strategy returns None for odd prices."""
        result = self.strategy.on_tick({"price": 41})
        assert result is None

    def test_buy_signal_for_zero_price(self):
        """Test that strategy returns buy signal for price 0."""
        result = self.strategy.on_tick({"price": 0})
        assert result == {"side": "buy", "qty": 1}

    def test_buy_signal_for_negative_even_price(self):
        """Test that strategy returns buy signal for negative even prices."""
        result = self.strategy.on_tick({"price": -10})
        assert result == {"side": "buy", "qty": 1} 