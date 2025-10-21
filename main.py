"""
Polymarket Arbitrage Tool
Main entry point
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.gui.main_window import run_gui
from src.utils.logger import setup_logger

logger = setup_logger("main")


def main():
    """Main entry point"""
    logger.info("Starting Polymarket Arbitrage Tool...")
    logger.info("Mode: Demo (fake money)")
    logger.info("="*50)
    
    try:
        run_gui()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
