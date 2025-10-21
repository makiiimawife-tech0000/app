# ⚡ Polymarket Arbitrage Bot

**Automated arbitrage trading bot for Polymarket prediction markets.**

Real-time price monitoring • Automatic opportunity detection • Safe demo mode

---

## 🚀 Installation (Windows Only)

### Step 1: Install
**Double-click:**
```
INSTALL_AND_SETUP.bat
```

The installer will:
- ✅ Check for Python (helps install if missing)
- ✅ Install all requirements (~100MB, 2-3 minutes)
- ✅ Create desktop shortcut
- ✅ Launch the app

### Step 2: Done!
Use the desktop shortcut to open the app anytime:
```
Desktop → "Polymarket Arbitrage Bot"
```

---

## 📖 How to Use

1. **Markets load automatically** (2-5 seconds)
2. **Search** for a market (e.g., "Trump", "Bitcoin", "AI")
3. **Click** on a market to select it
4. **Click "▶ Start Monitoring"**
5. **Watch** real-time prices from Polymarket
6. **Arbitrage detected?** App auto-executes with demo money

---

## 💰 What is Arbitrage?

When buying **YES + NO shares < $1.00**, you can profit by:

```
1. Buy YES share at $0.47
2. Buy NO share at $0.50
3. Merge positions → receive $1.00
4. Profit: $1.00 - $0.97 - fees = ~$0.01
```

The bot automatically finds and executes these opportunities.

---

## ✨ Features

- ✅ **Real-time prices** from Polymarket API
- ✅ **Auto-detection** of arbitrage opportunities
- ✅ **Demo mode** - fake money, real prices
- ✅ **One-click install** - no manual setup
- ✅ **Desktop shortcut** - easy access
- ✅ **Clean GUI** - professional interface

---

## 🎮 Demo Mode

**Current mode: DEMO (Safe Testing)**

- Uses **REAL** Polymarket market data
- Trades with **FAKE** money ($1000 starting balance)
- 100% safe, no risk, no login required
- Perfect for learning and testing strategies

---

## ⚙️ Configuration

Edit `app/config.yaml`:

```yaml
trading:
  min_profit_threshold: 0.01  # Min $0.01 profit
  trading_fee: 0.02           # 2% Polymarket fee
  gas_estimate: 0.01          # Gas cost

demo:
  initial_balance: 1000.0     # Starting balance

ui:
  auto_execute: true          # Auto-trade
```

---

## 📂 Project Structure

```
polymarket-arbitrage-bot/
│
├── INSTALL_AND_SETUP.bat    ← DOUBLE-CLICK TO INSTALL
├── README.md                ← This file
│
└── app/                     ← Everything lives here
    ├── launcher.bat         ← Run the app
    ├── main.py              ← Entry point
    ├── config.yaml          ← Settings
    ├── requirements.txt     ← Dependencies
    │
    ├── src/                 ← Source code
    │   ├── core/            ← Trading logic
    │   ├── gui/             ← User interface  
    │   └── utils/           ← Utilities
    │
    └── docs/                ← Documentation
```

See `STRUCTURE.txt` for detailed file tree.

---

## 🐛 Troubleshooting

**Markets not loading?**
- Check internet connection
- Click "🔄 Refresh" button

**"No module named PyQt6" error?**
- Run `INSTALL_AND_SETUP.bat` again

**Python not found?**
- Install Python 3.11+ from python.org
- ⚠️ Check "Add Python to PATH" during install
- Run installer again

**Installer won't run?**
- Right-click `INSTALL_AND_SETUP.bat`
- Select "Run as Administrator"

---

## 📚 Documentation

Full documentation in `app/docs/`:
- **START_HERE.txt** - Quick start guide
- **HOW_TO_INSTALL.md** - Detailed installation
- **QUICK_REFERENCE.md** - Usage cheat sheet
- **PROJECT_INFO.txt** - Technical details

---

## 🔒 Safety

**Demo Mode:**
- ✅ No real money
- ✅ No login required
- ✅ No risk whatsoever
- ✅ Safe to experiment

**Real Mode (Not Implemented):**
- ⚠️ Would require API keys
- ⚠️ Would use real money
- ⚠️ Has transaction costs
- ⚠️ Test thoroughly in demo first

---

## 🛠️ Requirements

- Windows 10/11
- Python 3.11+
- ~100MB disk space
- Internet connection

---

## ⚠️ Disclaimer

This software is for **educational purposes only**.

- Demo mode uses fake money - safe for learning
- Real trading involves financial risk
- Not financial advice
- Use at your own risk

---

## 📄 License

MIT License - Free to use and modify

---

**Built with Python • PyQt6 • Polymarket API**

*Happy arbitraging! 💰*
