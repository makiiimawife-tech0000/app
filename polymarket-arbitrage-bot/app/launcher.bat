@echo off
REM ============================================
REM  Polymarket Arbitrage Bot - Launcher
REM ============================================

title Polymarket Arbitrage Bot

REM Check dependencies
python -c "import PyQt6" 2>nul
if errorlevel 1 (
    echo.
    echo ========================================
    echo   MISSING DEPENDENCIES
    echo ========================================
    echo.
    echo Please run the installer:
    echo INSTALL_AND_SETUP.bat
    echo.
    pause
    exit /b 1
)

REM Launch app
echo.
echo Starting Polymarket Arbitrage Bot...
echo.
python main.py

REM Keep window open on error
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERROR OCCURRED
    echo ========================================
    echo.
    echo Check the error message above
    echo.
    pause
)
