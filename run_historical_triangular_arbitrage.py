import pandas as pd

# --- CONFIG ---
THRESHOLD = 0.05  # percent
BTC_CSV = "data/BTCUSDT-1m-2025-07-13.csv"
SOL_CSV = "data/SOLUSDT-1m-2025-07-13.csv"
SOLBTC_CSV = "data/SOLBTC-1m-2025-07-13.csv"

# --- LOAD DATA ---
def load_csv(path, price_col_name):
    data = pd.read_csv(
        path,
        header=None,
        names=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ]
    )
    # Convert microseconds to milliseconds for pandas
    close_time_ms = (data["close_time"] // 1000).astype(int)
    df = pd.DataFrame({
        "timestamp": pd.to_datetime(close_time_ms, unit="ms"),
        price_col_name: data["close"].astype(float)
    })
    return df

btc = load_csv(BTC_CSV, "BTCUSDT")
sol = load_csv(SOL_CSV, "SOLUSDT")
solbtc = load_csv(SOLBTC_CSV, "SOLBTC")

# Merge on timestamp (inner join)
df = btc.merge(sol, on="timestamp").merge(solbtc, on="timestamp")

# --- TRIANGULAR ARBITRAGE BACKTEST ---
trades = []
for i, row in df.iterrows():
    btc_usdt = row["BTCUSDT"]
    sol_usdt = row["SOLUSDT"]
    sol_btc = row["SOLBTC"]
    implied_sol_usdt = sol_btc * btc_usdt
    spread = implied_sol_usdt - sol_usdt
    spread_pct = (spread / sol_usdt) * 100
    if abs(spread_pct) > THRESHOLD:
        trades.append({
            "timestamp": row["timestamp"],
            "spread_pct": abs(spread_pct),
            "spread": abs(spread),
            "sol_usdt": sol_usdt,
            "implied_sol_usdt": implied_sol_usdt,
            "direction": "forward" if spread > 0 else "reverse"
        })

# --- SUMMARY ---
print(f"Triangular Arbitrage Backtest (Threshold: {THRESHOLD:.2f}%)")
print(f"Total periods checked: {len(df)}")
print(f"Number of arbitrage trades: {len(trades)}")
if trades:
    print("First 5 trades:")
    for t in trades[:5]:
        print(f"  {t['timestamp']} | Spread: {t['spread_pct']:.3f}% | Dir: {t['direction']} | SOL/USDT: {t['sol_usdt']:.2f} | Implied: {t['implied_sol_usdt']:.2f}") 