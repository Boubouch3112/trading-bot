#!/usr/bin/env python3
"""
Checks both BTC cross-exchange (Binance vs Kraken) and SOL triangular arbitrage (on Binance) every 10 seconds.
"""
import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.data_fetcher import DataFetcher

def main():
    fetcher = DataFetcher()
    trades = []  # List to store all virtual trades
    print("🚀 Multi-Arbitrage Monitor (BTC cross-exchange & SOL triangle)")
    print("=" * 60)
    print("Checks every 5 seconds. Press Ctrl+C to stop.")
    print()
    try:
        while True:
            print("\n--- BTC Cross-Exchange Arbitrage (Binance vs Kraken) ---")
            binance_price, kraken_price = fetcher.get_both_prices()
            if binance_price and kraken_price:
                spread_info = fetcher.calculate_spread(binance_price, kraken_price)
                print(f"Binance BTC/USDT: ${binance_price:,.2f}")
                print(f"Kraken  BTC/USDT: ${kraken_price:,.2f}")
                print(f"Spread: ${spread_info['spread']:.2f} ({spread_info['spread_pct']:.3f}%)")
                if float(spread_info['spread_pct']) > 0.2:
                    print(f"🚨 BTC Arbitrage Opportunity! Buy on {spread_info['lower_exchange']}, sell on {spread_info['higher_exchange']}")
                    trades.append({
                        "type": "BTC",
                        "buy_exchange": spread_info['lower_exchange'],
                        "sell_exchange": spread_info['higher_exchange'],
                        "spread_pct": float(spread_info['spread_pct']),
                        "spread": float(spread_info['spread']),
                        "buy_price": float(spread_info['lower_price']),
                        "sell_price": float(spread_info['higher_price']),
                        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                    })
            else:
                print("Could not fetch both BTC/USDT prices.")

            print("\n--- SOL Triangular Arbitrage (on Binance) ---")
            fetcher.check_sol_triangular_arbitrage(min_spread_pct=0.4, trades=trades)

            print("\nWaiting 5 seconds...")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Stopping multi-arbitrage monitor.")
        print(f"\nSummary: {len(trades)} trades would have been made.")
        for t in trades:
            print(t)

if __name__ == "__main__":
    main() 