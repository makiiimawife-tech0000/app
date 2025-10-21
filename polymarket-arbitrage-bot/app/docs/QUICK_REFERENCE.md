# ⚡ Quick Reference Guide

## 🚀 Installation (First Time Only)

### Windows
```
Double-click: INSTALL_AND_SETUP.bat
```

### Mac/Linux
```bash
./INSTALL_AND_SETUP.sh
```

---

## 🎮 Running the App

### Windows
- **Desktop shortcut:** "Polymarket Arbitrage Bot"
- **Or double-click:** `launcher.bat`

### Mac/Linux
- **Run:** `./launcher.sh`

---

## 📊 Using the App

| Step | Action |
|------|--------|
| 1 | Wait for markets to load (2-5 sec) |
| 2 | Search for a market in the search box |
| 3 | Click on a market to select it |
| 4 | Click "▶ Start Monitoring" |
| 5 | Watch real-time prices update |
| 6 | When arbitrage detected, it auto-executes |
| 7 | Check your balance and profit at bottom |

---

## 🎯 What to Look For

**Arbitrage opportunity appears when:**
```
YES + NO + fees < $1.00
```

**Example:**
```
YES: $0.47
NO:  $0.50
────────────
Total: $0.97 + 2% fee + $0.01 gas = $0.99
Profit: $0.01 (1% gain)
```

---

## ⚙️ Configuration

Edit `config.yaml` to change:
- `min_profit_threshold` - Minimum profit to execute
- `trading_fee` - Polymarket fee (2%)
- `initial_balance` - Demo starting balance
- `auto_execute` - Auto-trade on arbitrage

---

## 🔍 Monitoring Tips

1. **Popular markets** - More liquidity, better opportunities
2. **Watch the spread** - Smaller = fewer opportunities
3. **Check frequency** - Prices update every 2 seconds
4. **Multiple markets** - Stop and select different markets to compare

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Markets not loading | Click "🔄 Refresh" button |
| Prices not updating | Stop and restart monitoring |
| Dependencies missing | Run `INSTALL_AND_SETUP.bat` again |
| Python not found | Install Python 3.11+ from python.org |

---

## 📂 Project Files

```
INSTALL_AND_SETUP.bat/sh  ← Run this first!
launcher.bat/sh           ← Use this to start app
START_HERE.txt            ← Read this first
README.md                 ← Full documentation
config.yaml               ← Settings
requirements.txt          ← Dependencies list
```

---

## 💡 Key Features

- ✅ Real-time Polymarket prices
- ✅ Automatic arbitrage detection
- ✅ Demo mode (fake money)
- ✅ Desktop shortcut
- ✅ One-click install
- ✅ Clean modern GUI

---

## 🎮 Demo Mode

**What it means:**
- Uses **REAL** Polymarket market data
- Uses **FAKE** money for trading
- 100% safe, no risk
- Perfect for learning and testing

**Stats tracked:**
- Balance (starts at $1000)
- Total profit
- Number of trades
- All trades logged

---

## 🔒 Safety

**Demo Mode (Current):**
- ✅ No real money
- ✅ No login required
- ✅ No risk
- ✅ Safe to experiment

**Real Mode (Future):**
- ⚠️ Would use real money
- ⚠️ Requires API keys
- ⚠️ Has transaction costs
- ⚠️ Test in demo first!

---

## 📞 Need Help?

1. Check `START_HERE.txt`
2. Read `HOW_TO_INSTALL.md`
3. See full `README.md`
4. Check `logs/` folder for errors

---

**Happy arbitraging! 💰**
