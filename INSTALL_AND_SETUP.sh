#!/bin/bash
# ============================================
#  Polymarket Arbitrage Bot - Linux/Mac Installer
#  Run: chmod +x INSTALL_AND_SETUP.sh && ./INSTALL_AND_SETUP.sh
# ============================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo
echo "========================================"
echo "  POLYMARKET ARBITRAGE BOT"
echo "  Linux/Mac Installer"
echo "========================================"
echo

# ============================================
# Check Python
# ============================================
echo -e "${BLUE}[1/4] Checking Python...${NC}"
echo

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}[OK] Python3 found!${NC}"
    python3 --version
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo -e "${GREEN}[OK] Python found!${NC}"
    python --version
else
    echo -e "${RED}[X] Python NOT installed!${NC}"
    echo
    echo "Please install Python 3.11+ first:"
    echo
    echo "Ubuntu/Debian:"
    echo "  sudo apt update && sudo apt install python3 python3-pip"
    echo
    echo "CentOS/RHEL:"
    echo "  sudo yum install python3 python3-pip"
    echo
    echo "macOS:"
    echo "  brew install python3"
    echo "  # Or download from: https://www.python.org/downloads/"
    echo
    exit 1
fi

echo

# ============================================
# Check pip
# ============================================
echo -e "${BLUE}[2/4] Checking pip...${NC}"

if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
    echo -e "${GREEN}[OK] pip3 found!${NC}"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
    echo -e "${GREEN}[OK] pip found!${NC}"
else
    echo -e "${YELLOW}[!] Installing pip...${NC}"
    $PYTHON_CMD -m ensurepip --default-pip
    PIP_CMD="$PYTHON_CMD -m pip"
fi

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
$PIP_CMD install --upgrade pip --quiet

echo -e "${GREEN}[OK] Ready!${NC}"
echo

# ============================================
# Install packages
# ============================================
echo -e "${BLUE}[3/4] Installing packages (~50MB, 1-2 min)...${NC}"
echo
echo "Installing core dependencies (demo mode)..."
echo

cd polymarket-arbitrage-bot/app

$PIP_CMD install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[!] Trying individual install...${NC}"
    $PIP_CMD install PyQt6
    $PIP_CMD install aiohttp
    $PIP_CMD install pyyaml
    $PIP_CMD install python-dotenv
fi

cd ../..

echo
echo -e "${GREEN}[OK] Packages installed!${NC}"
echo

# ============================================
# Create launcher script
# ============================================
echo -e "${BLUE}[4/4] Creating launcher script...${NC}"
echo

cat > polymarket-arbitrage-bot/app/launcher.sh << 'EOF'
#!/bin/bash
# ============================================
#  Polymarket Arbitrage Bot - Launcher
# ============================================

# Change to the directory where this script is located
cd "$(dirname "$0")"

# Check dependencies
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo
    echo "========================================"
    echo "   PYTHON NOT FOUND"
    echo "========================================"
    echo
    echo "Please install Python 3.11+ and try again"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

$PYTHON_CMD -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo
    echo "========================================"
    echo "   MISSING DEPENDENCIES"
    echo "========================================"
    echo
    echo "Please run the installer:"
    echo "./INSTALL_AND_SETUP.sh"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Launch app
echo
echo "Starting Polymarket Arbitrage Bot..."
echo
$PYTHON_CMD main.py

# Keep terminal open on error
if [ $? -ne 0 ]; then
    echo
    echo "========================================"
    echo "   ERROR OCCURRED"
    echo "========================================"
    echo
    echo "Check the error message above"
    echo
    read -p "Press Enter to exit..."
fi
EOF

chmod +x polymarket-arbitrage-bot/app/launcher.sh

echo -e "${GREEN}[OK] Launcher script created!${NC}"
echo

# ============================================
# Try to create desktop shortcut (optional)
# ============================================
if [ -d "$HOME/Desktop" ]; then
    echo -e "${BLUE}Creating desktop shortcut...${NC}"
    
    SCRIPT_DIR="$(pwd)"
    
    cat > "$HOME/Desktop/Polymarket Arbitrage Bot.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Polymarket Arbitrage Bot
Comment=Real-time arbitrage detection and execution
Exec=$SCRIPT_DIR/polymarket-arbitrage-bot/app/launcher.sh
Icon=applications-games
Path=$SCRIPT_DIR/polymarket-arbitrage-bot/app
Terminal=true
Categories=Office;Finance;
EOF
    
    chmod +x "$HOME/Desktop/Polymarket Arbitrage Bot.desktop"
    echo -e "${GREEN}[OK] Desktop shortcut created!${NC}"
else
    echo -e "${YELLOW}[!] Desktop folder not found, skipping shortcut${NC}"
fi

echo

# ============================================
# Done!
# ============================================
echo
echo "========================================"
echo "   INSTALLATION COMPLETE!"
echo "========================================"
echo
echo -e "${GREEN}✓ Python found and ready${NC}"
echo -e "${GREEN}✓ All packages installed${NC}"
echo -e "${GREEN}✓ Launcher script created${NC}"
echo

if [ -f "$HOME/Desktop/Polymarket Arbitrage Bot.desktop" ]; then
    echo -e "${GREEN}✓ Desktop shortcut created${NC}"
    echo
    echo "To run the bot:"
    echo "• Double-click desktop shortcut"
    echo "• Or run: ./polymarket-arbitrage-bot/app/launcher.sh"
else
    echo "To run the bot:"
    echo "• Run: ./polymarket-arbitrage-bot/app/launcher.sh"
fi

echo
echo "========================================"
echo

echo "Launching in 3 seconds..."
sleep 3

cd polymarket-arbitrage-bot/app
./launcher.sh