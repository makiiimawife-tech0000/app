# ⚡ Polymarket Arbitrage Bot

**Automated arbitrage trading bot for Polymarket prediction markets.**

Real-time price monitoring • Auto-detection • Safe demo mode

---

## 🚀 Installation

**Go to the parent folder and double-click:**
```
INSTALL_AND_SETUP.bat
```

That's it! The installer will:
- ✅ Check for Python
- ✅ Install all packages (~100MB)
- ✅ Create desktop shortcut
- ✅ Launch the app

---

## 🎮 Running the App

**After installation:**
- Use desktop shortcut: "Polymarket Arbitrage Bot"
- Or double-click: `app\launcher.bat`

---

## 💰 How to Use

1. Wait for markets to load (2-5 sec)
2. Search for a market (e.g., "Trump", "Bitcoin")
3. Click a market to select it
4. Click "▶ Start Monitoring"
5. Watch real-time prices from Polymarket
6. Arbitrage detected → Auto-executes with demo money
7. Check your profits!

---

## 📊 What is Arbitrage?

When YES + NO shares cost less than $1.00:

```
Buy YES: $0.47
Buy NO:  $0.50
─────────────
Total:   $0.97
Merge:   $1.00
Profit:  $0.03 (minus fees)
```

The bot finds and executes these automatically.

---

## ✨ Features

- ✅ Real-time Polymarket prices
- ✅ Automatic opportunity detection
- ✅ Demo mode (fake money, real prices)
- ✅ One-click installation
- ✅ Desktop shortcut
- ✅ Clean modern interface

---

## 🎮 Demo Mode

**Current mode: DEMO**

- Uses REAL Polymarket data
- Trades with FAKE money ($1000)
- 100% safe, no risk
- No login required
- Perfect for learning

---

## ⚙️ Settings

Edit `app/config.yaml`:

```yaml
trading:
  min_profit_threshold: 0.01  # Minimum profit
  trading_fee: 0.02           # 2% fee
  
demo:
  initial_balance: 1000.0     # Starting balance
  
ui:
  auto_execute: true          # Auto-trade
```

---

## 📂 Structure

```
polymarket-arbitrage-bot/
├── README.md
├── START_HERE.txt
│
└── app/
    ├── launcher.bat      ← Run this
    ├── main.py
    ├── config.yaml
    ├── requirements.txt
    │
    ├── src/
    │   ├── core/         ← Trading logic
    │   ├── gui/          ← Interface
    │   └── utils/        ← Utilities
    │
    └── docs/             ← Documentation
```

---

## 🐛 Troubleshooting

**Python not found?**
- Install Python 3.11+ from python.org
- ⚠️ Check "Add Python to PATH"
- Run installer again

**Packages won't install?**
- Right-click installer → "Run as Administrator"

**Markets not loading?**
- Check internet connection
- Click "🔄 Refresh"

**Need help?**
- Read: `START_HERE.txt`
- Check: `app/docs/` folder

---

## 🔒 Safety

**Demo Mode:**
- ✅ No real money
- ✅ No login
- ✅ No risk
- ✅ Safe testing

**Real Mode (Not Available):**
- ⚠️ Would use real money
- ⚠️ Requires API keys
- ⚠️ Has costs

---

## 📄 License

MIT - Free to use

---

**Built with Python • PyQt6 • Polymarket API**

*Happy arbitraging! 💰*
