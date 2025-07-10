# Trading Bot

A Python-based trading strategy bot for learning purposes. This project demonstrates basic algorithmic trading concepts with a simple strategy implementation.

## Features

- Simple trading strategy based on price patterns
- Dockerized for easy deployment
- Testable architecture
- Extensible design for adding more complex strategies

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd trading-bot
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the strategy**
   ```bash
   python src/trading_bot/strategy.py
   ```

### Docker

1. **Build the image**
   ```bash
   docker build -t trading-bot .
   ```

2. **Run the container**
   ```bash
   docker run trading-bot
   ```

## Project Structure

```
trading-bot/
├── src/trading_bot/     # Main strategy code
│   ├── __init__.py
│   └── strategy.py      # Core strategy logic
├── tests/               # Test files
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Current Strategy

The current strategy is a simple example that:
- Takes price data as input
- Returns a "buy" signal for even prices
- Returns "no action" for odd prices

This is just a placeholder - replace with your actual trading logic!

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is for educational purposes.
