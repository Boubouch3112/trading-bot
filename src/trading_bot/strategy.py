from datetime import datetime, timezone

class Strategy:
    def on_tick(self, data):
        # TODO: replace with real logic
        if data["price"] % 2 == 0:
            return {"side": "buy", "qty": 1}
        return None

if __name__ == "__main__":
    strat = Strategy()
    print(f"{datetime.now(timezone.utc)} | Example tick ->", strat.on_tick({"price": 42}))