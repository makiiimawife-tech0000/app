@echo off
REM ============================================
REM  Polymarket Arbitrage Bot - Launcher
REM ============================================

REM Admin rights not required for running the application

title Polymarket Arbitrage Bot

REM Change to the directory where this script is located
cd /d "%~dp0"

REM Check dependencies
python -c "import PyQt6, aiohttp, yaml" 2>nul
if errorlevel 1 (
    echo.
    echo ========================================
    echo   MISSING DEPENDENCIES
    echo ========================================
    echo.
    echo Please run the installer first:
    echo %~dp0..\..\INSTALL_AND_SETUP.bat
    echo.
    echo Or install manually:
    echo pip install --user PyQt6 aiohttp pyyaml python-dotenv
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
