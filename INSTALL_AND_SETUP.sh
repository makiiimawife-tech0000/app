#!/bin/bash
# ============================================
#  Polymarket Arbitrage Bot - Full Setup
#  Run this to install everything!
# ============================================

clear
echo ""
echo "========================================"
echo "  POLYMARKET ARBITRAGE BOT"
echo "  Automatic Setup Wizard"
echo "========================================"
echo ""
sleep 1

# ============================================
# Step 1: Check if Python is installed
# ============================================
echo "[Step 1/4] Checking for Python..."
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[X] Python 3 is NOT installed!"
    echo ""
    echo "Please install Python 3.11+ first:"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip python3-venv"
    echo ""
    echo "macOS:"
    echo "  brew install python3"
    echo ""
    echo "Then run this script again."
    echo ""
    exit 1
fi

echo "[OK] Python is installed!"
python3 --version
echo ""
sleep 1

# ============================================
# Step 2: Upgrade pip
# ============================================
echo "[Step 2/4] Upgrading pip..."
echo ""
python3 -m pip install --upgrade pip --quiet
echo "[OK] Pip is ready!"
echo ""
sleep 1

# ============================================
# Step 3: Install dependencies
# ============================================
echo "[Step 3/4] Installing required packages..."
echo ""
echo "This may take 2-3 minutes..."
echo ""

python3 -m pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo ""
    echo "[X] Installation failed! Trying individual packages..."
    echo ""
    python3 -m pip install PyQt6
    python3 -m pip install aiohttp
    python3 -m pip install pyyaml
    python3 -m pip install python-dotenv
    python3 -m pip install py-clob-client
    python3 -m pip install web3
fi

echo ""
echo "[OK] All packages installed!"
echo ""
sleep 1

# ============================================
# Step 4: Create launcher script
# ============================================
echo "[Step 4/4] Creating launcher script..."
echo ""

cat > launcher.sh << 'EOF'
#!/bin/bash
# Polymarket Arbitrage Bot Launcher

# Check dependencies
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "  MISSING DEPENDENCIES!"
    echo "========================================"
    echo ""
    echo "Please run: ./INSTALL_AND_SETUP.sh"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Launch app
echo "Starting Polymarket Arbitrage Bot..."
echo ""
python3 main.py

# Keep terminal open on error
if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "  ERROR OCCURRED"
    echo "========================================"
    echo ""
    read -p "Press Enter to exit..."
fi
EOF

chmod +x launcher.sh

echo "[OK] Launcher created!"
echo ""

# ============================================
# Try to create desktop shortcut (optional)
# ============================================
if [ -d "$HOME/Desktop" ]; then
    echo "Creating desktop shortcut..."
    
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    
    cat > "$HOME/Desktop/Polymarket-Arbitrage-Bot.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Polymarket Arbitrage Bot
Comment=Real-time arbitrage trading
Exec=$SCRIPT_DIR/launcher.sh
Path=$SCRIPT_DIR
Icon=utilities-terminal
Terminal=true
Categories=Finance;Trading;
EOF
    
    chmod +x "$HOME/Desktop/Polymarket-Arbitrage-Bot.desktop"
    echo "[OK] Desktop shortcut created!"
fi

# ============================================
# Setup Complete!
# ============================================
echo ""
echo "========================================"
echo "  SETUP COMPLETE!"
echo "========================================"
echo ""
echo "You can now run the app with:"
echo ""
echo "  ./launcher.sh"
echo ""

if [ -f "$HOME/Desktop/Polymarket-Arbitrage-Bot.desktop" ]; then
    echo "Or use the desktop shortcut!"
    echo ""
fi

echo "========================================"
echo ""
echo "Starting the app in 3 seconds..."
sleep 3

# Launch the app
./launcher.sh
