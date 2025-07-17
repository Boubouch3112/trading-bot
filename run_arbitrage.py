#!/usr/bin/env python3
"""
Simple arbitrage bot that monitors BTC/USDT prices on Binance and Bitget
"""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.strategy import ArbitrageStrategy
from trading_bot.data_fetcher import DataFetcher

def main():
    print("🚀 Starting BTC Arbitrage Bot (Binance vs Kraken)")
    print("=" * 50)
    
    # Test the data fetcher first
    print("🔍 Testing API connections...")
    fetcher = DataFetcher()
    binance_price, kraken_price = fetcher.get_both_prices()
    
    if not binance_price or not kraken_price:
        print("❌ Failed to connect to exchanges. Check your internet connection.")
        return
    
    print("✅ Connected to both exchanges!")
    print(f"   Binance: ${binance_price:,.2f}")
    print(f"   Kraken:  ${kraken_price:,.2f}")
    
    # Calculate initial spread
    spread_info = fetcher.calculate_spread(binance_price, kraken_price)
    print(f"📊 Current spread: {spread_info['spread_pct']:.3f}%")
    print()
    
    # Create arbitrage strategy (0.2% minimum spread)
    strategy = ArbitrageStrategy(min_spread_pct=0.2)
    
    print("🔄 Starting monitoring loop...")
    print("   Press Ctrl+C to stop")
    print()
    
    try:
        while True:
            # Create dummy tick data (we'll fetch real data in the strategy)
            tick_data = {"timestamp": time.time()}
            
            # Run the strategy
            signal = strategy.on_tick(tick_data)
            
            if signal:
                print(f"🎯 ARBITRAGE OPPORTUNITY FOUND!")
                print(f"   Buy: {signal['buy_exchange']} at ${signal['buy_price']:,.2f}")
                print(f"   Sell: {signal['sell_exchange']} at ${signal['sell_price']:,.2f}")
                print(f"   Spread: {signal['spread_pct']:.3f}%")
                print(f"   Quantity: {signal['qty']} BTC")
                print("   💡 In a real bot, you would execute these trades here!")
                print()
            else:
                # Show current prices on every check
                binance_price, kraken_price = fetcher.get_both_prices()
                if binance_price and kraken_price:
                    spread_info = fetcher.calculate_spread(binance_price, kraken_price)
                    print(f"📊 Binance ${binance_price:,.2f} | Kraken ${kraken_price:,.2f} | Spread {spread_info['spread_pct']:.3f}%")
            
            # Wait 10 seconds between checks (to avoid hitting API limits)
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping arbitrage bot...")
        print("Thanks for using the arbitrage bot!")

if __name__ == "__main__":
    main() 