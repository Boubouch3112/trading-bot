import requests  # For making HTTP requests to APIs
import time  # For adding delays between requests
from typing import Dict, Optional, Tuple  # For type hints
from datetime import datetime, timezone  # For timestamps

class DataFetcher:
    def __init__(self):
        # API endpoints for getting BTC/USDT prices
        self.binance_url = "https://api.binance.com/api/v3/ticker/price"
        self.kraken_url = "https://api.kraken.com/0/public/Ticker"

    def get_binance_price(self, symbol: str) -> Optional[float]:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return float(response.json()['price'])
        except Exception as e:
            print(f"Error fetching {symbol} from Binance: {e}")
            return None

    def get_sol_triangular_prices(self):
        btc_usdt = self.get_binance_price("BTCUSDT")
        sol_usdt = self.get_binance_price("SOLUSDT")
        sol_btc = self.get_binance_price("SOLBTC")
        return btc_usdt, sol_usdt, sol_btc

    def check_sol_triangular_arbitrage(self, min_spread_pct=0.2, trades=None):
        btc_usdt, sol_usdt, sol_btc = self.get_sol_triangular_prices()
        if None in (btc_usdt, sol_usdt, sol_btc):
            print("Could not fetch all prices for SOL triangular arbitrage.")
            return

        assert isinstance(btc_usdt, float)
        assert isinstance(sol_usdt, float)
        assert isinstance(sol_btc, float)
        
        implied_sol_usdt = sol_btc * btc_usdt
        spread = implied_sol_usdt - sol_usdt
        spread_pct = (spread / sol_usdt) * 100

        print(f"SOL/USDT: {sol_usdt}")
        print(f"Implied SOL/USDT via BTC: {implied_sol_usdt}")
        print(f"Spread: {abs(spread):.4f} ({abs(spread_pct):.3f}%)")

        if abs(spread_pct) > min_spread_pct:
            print("🚨 SOL Triangular Arbitrage Opportunity Detected!")
            if trades is not None:
                trades.append({
                    "type": "SOL",
                    "direction": "forward" if spread > 0 else "reverse",
                    "spread_pct": abs(spread_pct),
                    "spread": abs(spread),
                    "sol_usdt": sol_usdt,
                    "implied_sol_usdt": implied_sol_usdt,
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                })
            if spread > 0:
                print("Buy SOL/USDT, Sell SOL/BTC for BTC, Sell BTC/USDT for USDT")
            else:
                print("Buy SOL/BTC for BTC, Buy BTC/USDT for USDT, Sell SOL/USDT")

    def get_binance_btc_usdt(self) -> Optional[float]:
        return self.get_binance_price("BTCUSDT")

    def get_kraken_btc_usdt(self) -> Optional[float]:
        try:
            response = requests.get(f"{self.kraken_url}?pair=XBTUSDT", timeout=5)
            response.raise_for_status()
            data = response.json()
            price = float(data['result']['XBTUSDT']['c'][0])
            return price
        except Exception as e:
            print(f"Error fetching Kraken price: {e}")
            return None

    def get_both_prices(self) -> Tuple[Optional[float], Optional[float]]:
        binance_price = self.get_binance_btc_usdt()
        kraken_price = self.get_kraken_btc_usdt()
        return binance_price, kraken_price

    def calculate_spread(self, price1: float, price2: float) -> Dict[str, float | str]:
        spread = abs(price1 - price2)
        spread_pct = (spread / min(price1, price2)) * 100
        return {
            "spread": spread,
            "spread_pct": spread_pct,
            "lower_price": min(price1, price2),
            "higher_price": max(price1, price2),
            "lower_exchange": "binance" if price1 < price2 else "kraken",
            "higher_exchange": "kraken" if price1 < price2 else "binance"
        }

# Test function to verify the data fetcher works
def test_data_fetcher():
    fetcher = DataFetcher()
    print("🔍 Testing API connections...")
    binance_price, kraken_price = fetcher.get_both_prices()
    if binance_price and kraken_price:
        print(f"✅ Binance BTC/USDT: ${binance_price:,.2f}")
        print(f"✅ Kraken BTC/USDT:  ${kraken_price:,.2f}")
        spread_info = fetcher.calculate_spread(binance_price, kraken_price)
        print(f"📊 Spread: ${spread_info['spread']:.2f} ({spread_info['spread_pct']:.3f}%)")
        print(f"💰 Buy on: {spread_info['lower_exchange']}")
        print(f"💰 Sell on: {spread_info['higher_exchange']}")
    else:
        print("❌ Failed to fetch prices from one or both exchanges")
    print("\n--- SOL Triangular Arbitrage Test ---")
    fetcher.check_sol_triangular_arbitrage(min_spread_pct=0.2)

if __name__ == "__main__":
    test_data_fetcher() 