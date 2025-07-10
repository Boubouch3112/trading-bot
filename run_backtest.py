#!/usr/bin/env python3
"""
Simple script to run backtesting on your trading strategy
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_bot.backtest import Backtest, create_sample_data
from trading_bot.strategy import Strategy

def main():
    print("🚀 Running Trading Bot Backtest")
    print("=" * 50)
    
    # Create sample data
    print("📊 Generating sample price data...")
    data = create_sample_data(days=60)  # 60 days of data
    print(f"Generated {len(data)} data points")
    print(f"Price range: ${data['price'].min():.2f} - ${data['price'].max():.2f}")
    print()
    
    # Run backtest
    print("⚡ Running backtest...")
    strategy = Strategy()
    backtest = Backtest(initial_capital=10000)
    results = backtest.run(data, strategy)
    
    # Display results
    print("📈 Backtest Results:")
    print(f"  Initial Capital: ${results['initial_capital']:,.2f}")
    print(f"  Final Equity:    ${results['final_equity']:,.2f}")
    print(f"  Total Return:    {results['total_return_pct']:+.2f}%")
    print(f"  Total Trades:    {results['total_trades']}")
    print(f"  Max Drawdown:    {results['max_drawdown_pct']:.2f}%")
    
    if results['trades']:
        print(f"\n📋 Recent Trades:")
        for trade in results['trades'][-5:]:  # Last 5 trades
            print(f"  {trade['timestamp'].date()} | {trade['side'].upper():4} | "
                  f"Price: ${trade['price']:6.2f} | Qty: {trade['qty']}")
    else:
        print("\n📋 No trades executed during backtest period")

if __name__ == "__main__":
    main() 