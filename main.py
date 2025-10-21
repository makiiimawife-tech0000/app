"""
⚡ Polymarket Arbitrage Bot
Real-time arbitrage detection and execution
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.gui.main_window import run_gui
from src.utils.logger import setup_logger

logger = setup_logger("arbitrage")


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("⚡ POLYMARKET ARBITRAGE BOT")
    logger.info("=" * 60)
    logger.info("Mode: DEMO (real prices, fake money)")
    logger.info("Fetching real-time data from Polymarket...")
    logger.info("=" * 60)
    
    try:
        run_gui()
    except KeyboardInterrupt:
        logger.info("\n\nShutdown requested by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
