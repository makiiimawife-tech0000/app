@echo off
REM ============================================
REM  Polymarket Arbitrage Bot - Installer
REM  Double-click to install everything!
REM ============================================

title Polymarket Arbitrage Bot - Installation
color 0A

echo.
echo ========================================
echo   POLYMARKET ARBITRAGE BOT
echo   Installation Wizard
echo ========================================
echo.
timeout /t 2 /nobreak >nul

REM ============================================
REM Step 1: Check Python
REM ============================================
echo [1/4] Checking Python installation...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is NOT installed!
    echo.
    echo Opening Python download page...
    echo.
    echo IMPORTANT:
    echo 1. Download Python 3.11 or newer
    echo 2. Run the installer
    echo 3. CHECK "Add Python to PATH"
    echo 4. Run this installer again
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found!
python --version
echo.

REM ============================================
REM Step 2: Upgrade pip
REM ============================================
echo [2/4] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] Ready!
echo.

REM ============================================
REM Step 3: Install packages
REM ============================================
echo [3/4] Installing packages...
echo.
echo This will take 2-3 minutes (~100MB download)
echo.

cd app
python -m pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo [!] Installation failed, trying individually...
    python -m pip install PyQt6
    python -m pip install aiohttp
    python -m pip install pyyaml
    python -m pip install python-dotenv
    python -m pip install py-clob-client
    python -m pip install web3
)

cd ..

echo.
echo [OK] All packages installed!
echo.

REM ============================================
REM Step 4: Create Desktop Shortcut
REM ============================================
echo [4/4] Creating desktop shortcut...
echo.

set SCRIPT_DIR=%~dp0

REM Create VBScript for shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Polymarket Arbitrage Bot.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%app\launcher.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%app" >> CreateShortcut.vbs
echo oLink.Description = "Polymarket Arbitrage Bot" >> CreateShortcut.vbs
echo oLink.IconLocation = "C:\Windows\System32\shell32.dll,21" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript CreateShortcut.vbs >nul
del CreateShortcut.vbs

echo [OK] Desktop shortcut created!
echo.

REM ============================================
REM Complete!
REM ============================================
echo.
echo ========================================
echo   INSTALLATION COMPLETE!
echo ========================================
echo.
echo Desktop shortcut created:
echo "Polymarket Arbitrage Bot"
echo.
echo Or run from:
echo app\launcher.bat
echo.
echo ========================================
echo.
echo Launching app in 3 seconds...
timeout /t 3 /nobreak >nul

start "" "%SCRIPT_DIR%app\launcher.bat"

echo.
timeout /t 2 /nobreak >nul
exit
