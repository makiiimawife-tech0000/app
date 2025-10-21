@echo off
REM ============================================
REM  Polymarket Arbitrage Bot - Full Setup
REM  Double-click this to install everything!
REM ============================================

title Polymarket Arbitrage Bot - Setup
color 0A

echo.
echo ========================================
echo   POLYMARKET ARBITRAGE BOT
echo   Automatic Setup Wizard
echo ========================================
echo.
timeout /t 2 /nobreak >nul

REM ============================================
REM Step 1: Check if Python is installed
REM ============================================
echo [Step 1/4] Checking for Python...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [X] Python is NOT installed!
    echo.
    echo ========================================
    echo   INSTALLING PYTHON
    echo ========================================
    echo.
    echo Opening Python download page...
    echo.
    echo Please:
    echo  1. Download Python 3.11 or newer
    echo  2. Run the installer
    echo  3. CHECK "Add Python to PATH"
    echo  4. Run this script again
    echo.
    start https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed!
python --version
echo.
timeout /t 1 /nobreak >nul

REM ============================================
REM Step 2: Upgrade pip
REM ============================================
echo [Step 2/4] Upgrading pip...
echo.
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [!] Warning: Could not upgrade pip, continuing anyway...
)
echo [OK] Pip is ready!
echo.
timeout /t 1 /nobreak >nul

REM ============================================
REM Step 3: Install dependencies
REM ============================================
echo [Step 3/4] Installing required packages...
echo.
echo This may take 2-3 minutes...
echo Installing: PyQt6, aiohttp, and others...
echo.

python -m pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo.
    echo [X] Installation failed! Trying individual packages...
    echo.
    python -m pip install PyQt6
    python -m pip install aiohttp
    python -m pip install pyyaml
    python -m pip install python-dotenv
    python -m pip install py-clob-client
    python -m pip install web3
)

echo.
echo [OK] All packages installed!
echo.
timeout /t 1 /nobreak >nul

REM ============================================
REM Step 4: Create Desktop Shortcut
REM ============================================
echo [Step 4/4] Creating desktop shortcut...
echo.

REM Get the current directory
set SCRIPT_DIR=%~dp0

REM Create VBScript to make shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Polymarket Arbitrage Bot.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%launcher.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "Polymarket Arbitrage Bot - Real-time trading" >> CreateShortcut.vbs
echo oLink.IconLocation = "C:\Windows\System32\shell32.dll,21" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Run the VBScript
cscript CreateShortcut.vbs >nul

REM Clean up
del CreateShortcut.vbs

echo [OK] Desktop shortcut created!
echo.

REM ============================================
REM Setup Complete!
REM ============================================
echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo You can now:
echo.
echo  1. Use the desktop shortcut:
echo     "Polymarket Arbitrage Bot"
echo.
echo  2. Or run from this folder:
echo     Double-click "launcher.bat"
echo.
echo ========================================
echo.
echo Starting the app in 3 seconds...
timeout /t 3 /nobreak >nul

REM Launch the app
start "" "%SCRIPT_DIR%launcher.bat"

echo.
echo Thank you for using Polymarket Arbitrage Bot!
echo.
timeout /t 2 /nobreak >nul
exit
