@echo off
REM ============================================
REM  Polymarket Arbitrage Bot - Launcher
REM ============================================

title Polymarket Arbitrage Bot

REM Check if dependencies are installed
python -c "import PyQt6" 2>nul
if errorlevel 1 (
    echo.
    echo ========================================
    echo   MISSING DEPENDENCIES!
    echo ========================================
    echo.
    echo Please run: INSTALL_AND_SETUP.bat
    echo.
    pause
    exit /b 1
)

REM Launch the application
echo Starting Polymarket Arbitrage Bot...
echo.
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERROR OCCURRED
    echo ========================================
    echo.
    pause
)
