@echo off
REM Windows setup script for Polymarket Arbitrage Bot

echo.
echo ========================================
echo   Polymarket Arbitrage Bot Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.11+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo [1/3] Python found:
python --version
echo.

echo [2/3] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [3/3] Installing dependencies...
python -m pip install -r requirements.txt
echo.

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo.
    echo Try running manually:
    echo   pip install PyQt6 aiohttp pyyaml python-dotenv py-clob-client web3
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo To run the app, execute:
echo   python main.py
echo.
echo Or just double-click: run.bat
echo.
pause
