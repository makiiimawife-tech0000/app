"""
⚡ Polymarket Arbitrage Bot
Real-time arbitrage detection and execution
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def check_dependencies():
    """Check if required dependencies are installed"""
    missing = []
    
    try:
        import PyQt6
    except ImportError:
        missing.append("PyQt6")
    
    try:
        import aiohttp
    except ImportError:
        missing.append("aiohttp")
    
    try:
        import yaml
    except ImportError:
        missing.append("pyyaml")
    
    if missing:
        print("\n" + "=" * 60)
        print("❌ MISSING DEPENDENCIES")
        print("=" * 60)
        print("\nThe following required packages are not installed:")
        for pkg in missing:
            print(f"  • {pkg}")
        print("\n📦 To install all dependencies, run:")
        print("\n  pip install -r requirements.txt")
        print("\nOr install individually:")
        print("\n  pip install PyQt6 aiohttp pyyaml python-dotenv")
        print("\n" + "=" * 60)
        print("\n💡 See INSTALL.md for detailed installation guide")
        print("=" * 60 + "\n")
        sys.exit(1)


def main():
    """Main entry point"""
    # Check dependencies first
    check_dependencies()
    
    # Import after checking dependencies
    from src.gui.main_window import run_gui
    from src.utils.logger import setup_logger
    
    logger = setup_logger("arbitrage")
    
    logger.info("=" * 60)
    logger.info("⚡ POLYMARKET ARBITRAGE BOT")
    logger.info("=" * 60)
    logger.info("Mode: DEMO (real prices, fake money)")
    logger.info("Fetching real-time data from Polymarket...")
    logger.info("=" * 60)
    
    try:
        # Check if config file exists
        from pathlib import Path
        config_path = Path(__file__).parent / "config.yaml"
        if not config_path.exists():
            logger.error(f"Configuration file not found: {config_path}")
            print(f"\n❌ ERROR: Configuration file missing!")
            print(f"Expected location: {config_path}")
            print(f"Please ensure config.yaml exists in the app directory.")
            sys.exit(1)
        
        run_gui()
    except KeyboardInterrupt:
        logger.info("\n\nShutdown requested by user")
        sys.exit(0)
    except ImportError as e:
        logger.error(f"Import error: {e}")
        print(f"\n❌ IMPORT ERROR: {e}")
        print(f"Please run the installer: INSTALL_AND_SETUP.bat")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        print(f"\n❌ APPLICATION ERROR: {e}")
        print(f"Check the log file for more details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
