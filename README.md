# Polymarket Arbitrage Tool 💰

**Windows desktop application for detecting and executing arbitrage opportunities on Polymarket.**

> Fast, simple, clean Python tool with desktop GUI - no web browser needed!

## What It Does

1. **Monitors** Polymarket markets for price inefficiencies
2. **Detects** when YES + NO shares cost less than $1.00
3. **Executes** buys both sides and merges for guaranteed profit
4. **Demo Mode** - Test with fake money (no login required)
5. **Real Mode** - Trade with your Polymarket account

## Features

- ✅ Clean Windows desktop GUI
- ✅ Market search and selection
- ✅ Real-time price monitoring
- ✅ Automatic arbitrage detection
- ✅ Demo mode (no risk, fake money)
- ✅ Real mode (your Polymarket account)
- ✅ Trade logging and profit tracking

## Installation

```bash
# Install Python 3.11+
# Download from python.org

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

## Usage

### Demo Mode (Default)
1. Launch app
2. Search for a market
3. Select market from list
4. Click "Start Monitoring"
5. Watch for arbitrage opportunities
6. App auto-executes with fake money
7. See simulated profits!

### Real Mode
1. Get Polymarket API credentials
2. Switch to "Real Mode" in app
3. Enter your credentials
4. Select market and start monitoring
5. App executes real trades for real profit

## Project Structure

```
polymarket-arbitrage-tool/
│
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── config.yaml            # Configuration
│
├── src/
│   ├── gui/
│   │   ├── main_window.py     # Main GUI window
│   │   └── styles.py          # UI styling
│   │
│   ├── core/
│   │   ├── market.py          # Market data fetching
│   │   ├── arbitrage.py       # Detection logic
│   │   ├── demo_mode.py       # Demo execution
│   │   └── real_mode.py       # Real execution
│   │
│   └── utils/
│       ├── logger.py          # Logging
│       └── config.py          # Config loader
│
└── README.md
```

## Requirements

- Python 3.11+
- Windows 10/11
- Internet connection
- For real mode: Polymarket account + API credentials

## Safety

- Demo mode uses fake money - completely safe
- Real mode: Start with small amounts ($10-50)
- All trades are logged
- Stop button works instantly

## License

MIT
