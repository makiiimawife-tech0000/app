# 🚀 Installation Guide

## Step 1: Install Python

Make sure you have **Python 3.11 or newer** installed.

Check your Python version:
```bash
python --version
```

If you don't have Python, download it from: https://www.python.org/downloads/

**⚠️ Important for Windows:** 
- Check "Add Python to PATH" during installation

---

## Step 2: Install Dependencies

Open a terminal/command prompt in the project folder and run:

### Windows (Command Prompt or PowerShell):
```bash
pip install -r requirements.txt
```

### If that doesn't work, try:
```bash
python -m pip install -r requirements.txt
```

### Or install packages individually:
```bash
pip install PyQt6
pip install aiohttp
pip install pyyaml
pip install python-dotenv
pip install py-clob-client
pip install web3
```

---

## Step 3: Run the Application

```bash
python main.py
```

---

## 🐛 Troubleshooting

### "pip is not recognized"
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### "No module named 'PyQt6'"
You didn't install dependencies. Go back to Step 2.

### Permission errors (Linux/Mac)
```bash
pip install --user -r requirements.txt
```

### Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
python main.py
```

---

## ✅ Verify Installation

After installing, verify PyQt6 works:

```bash
python -c "from PyQt6.QtWidgets import QApplication; print('✓ PyQt6 installed!')"
```

You should see: `✓ PyQt6 installed!`

---

## 📦 What Gets Installed

- **PyQt6** (~50MB) - Desktop GUI framework
- **aiohttp** - Async HTTP for API calls
- **pyyaml** - Configuration file parsing
- **python-dotenv** - Environment variables
- **py-clob-client** - Polymarket SDK
- **web3** - Blockchain library

**Total download:** ~100MB

---

## 🎮 First Run

After installation:
1. Run `python main.py`
2. Wait 2-5 seconds for markets to load
3. Select a market and click "▶ Start Monitoring"
4. Watch the magic happen!

---

**Need help?** Check README.md for usage guide.
