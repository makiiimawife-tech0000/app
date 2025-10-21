#!/bin/bash
# ============================================
# Polymarket Arbitrage Bot - Linux/Mac Installer
# ============================================

set -e  # Exit on any error

echo "========================================"
echo "  POLYMARKET ARBITRAGE BOT"
echo "  Linux/Mac Installer"
echo "========================================"
echo

# Check Python
echo "[1/4] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo
    echo "Please install Python 3.11+ first:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
    echo "  macOS:         brew install python3"
    echo
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $PYTHON_VERSION found"
echo

# Check pip
echo "[2/4] Checking pip..."
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip not found!"
    echo "Installing pip..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-pip
    elif command -v brew &> /dev/null; then
        brew install python3
    else
        echo "Please install pip manually"
        exit 1
    fi
fi
echo "✓ pip available"
echo

# Install packages
echo "[3/4] Installing packages (~50MB, 1-2 min)..."
echo
cd "$(dirname "$0")/polymarket-arbitrage-bot/app"

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

echo "Installing from requirements.txt..."
python3 -m pip install --user -r requirements.txt

if [ $? -ne 0 ]; then
    echo "⚠️  Trying individual install..."
    python3 -m pip install --user "PyQt6>=6.6.0"
    python3 -m pip install --user "aiohttp>=3.9.0"
    python3 -m pip install --user "pyyaml>=6.0.0"
    python3 -m pip install --user "python-dotenv>=1.0.0"
fi

echo "✓ Packages installed!"
echo

# Create launcher script
echo "[4/4] Creating launcher..."
cd "$(dirname "$0")"

cat > polymarket-arbitrage-bot/app/launcher.sh << 'EOF'
#!/bin/bash
# Polymarket Arbitrage Bot Launcher

cd "$(dirname "$0")"

# Check dependencies
python3 -c "import PyQt6, aiohttp, yaml" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies!"
    echo "Please run the installer first: ./install.sh"
    exit 1
fi

echo "Starting Polymarket Arbitrage Bot..."
python3 main.py
EOF

chmod +x polymarket-arbitrage-bot/app/launcher.sh

echo "✓ Launcher created!"
echo

echo "========================================"
echo "  INSTALLATION COMPLETE!"
echo "========================================"
echo
echo "To run the bot:"
echo "  cd polymarket-arbitrage-bot/app"
echo "  ./launcher.sh"
echo
echo "Or:"
echo "  cd polymarket-arbitrage-bot/app"
echo "  python3 main.py"
echo
echo "========================================"
echo

# Ask if user wants to run now
read -p "Run the bot now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd polymarket-arbitrage-bot/app
    ./launcher.sh
fi