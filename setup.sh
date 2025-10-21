#!/bin/bash
# Linux/Mac setup script for Polymarket Arbitrage Bot

echo ""
echo "========================================"
echo "  Polymarket Arbitrage Bot Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Install Python 3.11+ from your package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Mac: brew install python3"
    echo ""
    exit 1
fi

echo "[1/3] Python found:"
python3 --version
echo ""

echo "[2/3] Upgrading pip..."
python3 -m pip install --upgrade pip
echo ""

echo "[3/3] Installing dependencies..."
python3 -m pip install -r requirements.txt
echo ""

echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo "To run the app, execute:"
echo "  python3 main.py"
echo ""
