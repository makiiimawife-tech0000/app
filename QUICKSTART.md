# Quick Start Guide

## Installation

### 1. Install Python
Download and install Python 3.11 or later from [python.org](https://www.python.org/downloads/)

### 2. Install Dependencies
```bash
cd polymarket-arbitrage-tool
pip install -r requirements.txt
```

### 3. Run the Tool
```bash
python main.py
```

## Using the Tool

### Demo Mode (Default - No Login Required)

1. **Launch the app**
   ```bash
   python main.py
   ```

2. **Wait for markets to load**
   - The app automatically fetches markets from Polymarket
   - You'll see a list of active markets

3. **Search for a market**
   - Type in the search box (e.g., "Trump", "Bitcoin")
   - Click on a market to select it

4. **Start monitoring**
   - Click "▶ Start Monitoring"
   - Watch live prices update
   - App will detect arbitrage opportunities

5. **When arbitrage is detected**
   - You'll see: "⚠️ ARBITRAGE! Profit: $X.XX"
   - In demo mode, it auto-executes with fake money
   - Or click "⚡ Execute Once" to trade manually

6. **View results**
   - Activity log shows all trades
   - Status bar shows balance and profit
   - All with fake money!

### What You'll See

```
[12:34:01] Fetching markets from Polymarket...
[12:34:02] Loaded 50 markets
[12:34:05] Selected market: Will Trump win 2024?
[12:34:06] Started monitoring: Will Trump win 2024?
[12:34:10] [DEMO] YES: $0.47, NO: $0.50 (Total: $0.97)
[12:34:10] ⚠️ ARBITRAGE! Profit: $0.0194
[12:34:10] [DEMO] Buying YES share @ $0.47
[12:34:10] [DEMO] Buying NO share @ $0.50
[12:34:10] [DEMO] Merging positions...
[12:34:10] [DEMO] Trade complete! Profit: $0.0194
[12:34:10] [DEMO] New balance: $1000.02
```

## Demo vs Real Mode

### Demo Mode ✅ (Safe, No Risk)
- Uses fake $1000 balance
- Shows real Polymarket markets and prices
- Simulates trades instantly
- Perfect for learning and testing
- **No login required**
- **No real money**

### Real Mode ⚠️ (Coming in Phase 2)
- Uses your real Polymarket account
- Executes real trades
- Real money, real profit (or loss)
- Requires API credentials
- Start small ($10-50 recommended)

## Troubleshooting

### "No markets loading"
- Check internet connection
- Polymarket API might be temporarily down
- Click "🔄 Refresh" to try again

### "Can't install dependencies"
```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Then install again
pip install -r requirements.txt
```

### "PyQt6 won't install"
- Make sure you have Python 3.11+
- On Linux: `sudo apt-get install python3-pyqt6`
- On Windows: Should work with pip

## Next Steps

1. **Test in Demo Mode**
   - Select different markets
   - Watch for arbitrage opportunities
   - Learn how it works

2. **Understand the Strategy**
   - Arbitrage happens when YES + NO < $1.00
   - Buy both sides, merge for $1.00
   - Profit = $1.00 - (YES + NO + fees)

3. **When Ready for Real Mode**
   - Get Polymarket API credentials
   - Copy `.env.example` to `.env`
   - Add your credentials
   - Switch to Real Mode in app
   - Start with small amounts!

## Support

For issues or questions:
- Check the main README.md
- Review config.yaml for settings
- Check logs/ folder for detailed logs

## Safety Reminder

- Demo mode is completely safe (fake money)
- Real mode uses real money - be careful!
- Start small when going live
- Understand the risks
- Test thoroughly in demo first

Happy arbitraging! 🚀
