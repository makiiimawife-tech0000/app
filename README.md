# ⚡ Polymarket Arbitrage Bot

**Desktop application that detects and executes arbitrage opportunities on Polymarket.**

Real-time price monitoring • Automatic arbitrage detection • Demo mode with fake money

---

## 🎯 What It Does

This bot monitors Polymarket markets for **arbitrage opportunities** where buying YES + NO shares costs less than $1.00.

**The Strategy:**
1. 📊 Monitor market prices in real-time
2. 🔍 Detect when `YES + NO < $1.00` (after fees)
3. 💰 Buy both YES and NO shares
4. 🔄 Merge positions to receive $1.00
5. ✨ Keep the profit

**Current Mode:** Demo (real Polymarket prices, fake money)

---

## 🚀 Quick Start

### Installation

```bash
# Install Python 3.11+
# Download from python.org if needed

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

The GUI will open and automatically fetch markets from Polymarket.

### Usage

1. **Wait for markets to load** (2-5 seconds)
2. **Search and select a market** (e.g., "Trump", "Bitcoin")
3. **Click "▶ Start Monitoring"**
4. **Watch real-time prices** update from Polymarket
5. **When arbitrage detected**, app shows profit opportunity
6. **Auto-executes** with demo money (or click "⚡ Execute Now")

---

## ✨ Features

### Real Polymarket Integration
- ✅ Fetches live markets via Gamma API
- ✅ Real-time price updates via CLOB API
- ✅ Actual orderbook data
- ✅ ~2 second price refresh rate

### Arbitrage Detection
- ✅ Automatic opportunity detection
- ✅ Accounts for 2% trading fees
- ✅ Accounts for gas costs (~$0.01)
- ✅ Configurable profit threshold

### Demo Mode (Safe Testing)
- ✅ Uses real Polymarket prices
- ✅ Simulates order placement
- ✅ Starts with $1,000 fake money
- ✅ Tracks profits and trades
- ✅ No risk, no login required

### Clean Desktop GUI
- ✅ Market search and selection
- ✅ Live price display
- ✅ Arbitrage alerts
- ✅ Activity logging
- ✅ Trade statistics

---

## 📊 How Arbitrage Works

**Example:**
```
YES price:  $0.47
NO price:   $0.50
Total cost: $0.97

Trading fee (2%): $0.0194
Gas cost:         $0.01
Total cost:       $0.9994

Merge payout:     $1.00
Profit:           $0.0006 (0.06%)
```

The bot automatically detects these opportunities and executes trades.

---

## ⚙️ Configuration

Edit `config.yaml` to customize:

```yaml
trading:
  min_profit_threshold: 0.01    # Minimum $0.01 profit
  trading_fee: 0.02             # 2% Polymarket fee
  gas_estimate: 0.01            # Gas cost estimate
  
demo:
  initial_balance: 1000.0       # Starting demo balance
  
ui:
  auto_execute: true            # Auto-execute arbitrage
```

---

## 🏗️ Project Structure

```
polymarket-arbitrage-tool/
│
├── main.py                    # Entry point
├── config.yaml                # Configuration
├── requirements.txt           # Dependencies
│
└── src/
    ├── core/
    │   ├── market.py          # Polymarket API integration
    │   ├── arbitrage.py       # Detection algorithm
    │   └── demo_mode.py       # Demo trading
    │
    ├── gui/
    │   └── main_window.py     # Desktop interface
    │
    └── utils/
        ├── config.py          # Config loader
        └── logger.py          # Logging
```

---

## 🔒 Safety

### Demo Mode (Current)
- ✅ **100% safe** - uses fake money
- ✅ **No login required** - no API keys needed
- ✅ **Real prices** - from actual Polymarket
- ✅ **Perfect for learning** and testing strategies

### Real Mode (Future)
- ⚠️ Would use real money
- ⚠️ Requires API credentials
- ⚠️ Blockchain transaction costs
- ⚠️ Test thoroughly in demo first

---

## 📈 Performance

- **Market loading:** 2-5 seconds
- **Price updates:** Every 2 seconds (real-time)
- **Arbitrage detection:** < 1ms
- **Order execution:** Instant (demo mode)

---

## 🛠️ Requirements

- Python 3.11+
- Windows/Mac/Linux
- Internet connection
- ~50MB disk space

**Dependencies:**
- PyQt6 - Desktop GUI
- aiohttp - Async HTTP
- py-clob-client - Polymarket SDK
- web3 - Blockchain (future use)

---

## 📝 Example Session

```
[12:34:01] 🔄 Fetching markets from Polymarket...
[12:34:03] ✓ Loaded 50 active markets
[12:34:10] ✓ Selected: Will Trump win 2024?
[12:34:12] ▶ Monitoring started
[12:34:12] 📡 Fetching real-time prices from Polymarket...
[12:34:14] YES: $0.4732 | NO: $0.5101
[12:34:16] 🚨 ARBITRAGE OPPORTUNITY!
[12:34:16] 💰 Profit: $0.0127 (1.29%)
[12:34:16] ⚡ ARBITRAGE EXECUTED
[12:34:16]    💰 Profit: $0.0127
[12:34:16]    📊 Balance: $1000.01
```

---

## 🎮 Tips

1. **Start with popular markets** - they have better liquidity
2. **Monitor for a few minutes** - see how often opportunities appear
3. **Understand the fees** - 2% trading fee + gas significantly reduces profit
4. **Watch the spread** - tighter spreads = fewer opportunities
5. **Test different thresholds** - adjust `min_profit_threshold` in config

---

## 🐛 Troubleshooting

**Markets not loading?**
- Check internet connection
- Click "🔄 Refresh" button
- Check logs in `logs/` folder

**Prices not updating?**
- Stop and restart monitoring
- Polymarket API may be rate-limiting
- Check selected market is still active

**Dependencies won't install?**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📚 Learn More

**Polymarket:**
- [Polymarket Docs](https://docs.polymarket.com/)
- [CLOB API](https://docs.polymarket.com/#clob-api)

**Arbitrage:**
- Arbitrage = risk-free profit from price differences
- Works when YES + NO ≠ $1.00 (after fees)
- Requires fast execution in competitive markets

---

## 🤝 Contributing

This is a demo project for educational purposes. Feel free to:
- Fork and experiment
- Add new features
- Improve the algorithm
- Share your results

---

## ⚠️ Disclaimer

This software is for **educational purposes only**.

- Demo mode uses fake money - completely safe
- Real trading involves financial risk
- Not financial advice
- Use at your own risk
- Test thoroughly before using real money

---

## 📄 License

MIT License - Free to use and modify

---

**Built with Python • PyQt6 • Polymarket API**

*Happy arbitraging! 💰*
