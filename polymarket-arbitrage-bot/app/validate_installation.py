#!/usr/bin/env python3
"""
Installation Validator for Polymarket Arbitrage Bot
Validates that all components are properly installed and configured
"""
import sys
import asyncio
from pathlib import Path

def validate_dependencies():
    """Validate all required dependencies"""
    print("🔍 Validating dependencies...")
    
    required = {
        'PyQt6': 'GUI framework',
        'aiohttp': 'HTTP client for API calls',
        'yaml': 'Configuration file parser (pyyaml)',
        'dotenv': 'Environment variable loader (python-dotenv)'
    }
    
    missing = []
    
    for module, description in required.items():
        try:
            __import__(module)
            print(f"  ✓ {module} - {description}")
        except ImportError as e:
            if module == 'PyQt6' and ('libEGL' in str(e) or 'display' in str(e)):
                print(f"  ⚠ {module} - {description} (GUI not available in headless mode)")
            else:
                print(f"  ✗ {module} - {description} - MISSING")
                missing.append(module)
    
    return len(missing) == 0

def validate_files():
    """Validate all required files exist"""
    print("\n📁 Validating file structure...")
    
    required_files = [
        'main.py',
        'config.yaml',
        'requirements.txt',
        'launcher.bat',
        'src/__init__.py',
        'src/core/__init__.py',
        'src/core/arbitrage.py',
        'src/core/demo_mode.py',
        'src/core/market.py',
        'src/gui/__init__.py',
        'src/gui/main_window.py',
        'src/utils/__init__.py',
        'src/utils/config.py',
        'src/utils/logger.py'
    ]
    
    missing = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            missing.append(file_path)
    
    return len(missing) == 0

def validate_config():
    """Validate configuration loading"""
    print("\n⚙️ Validating configuration...")
    
    try:
        from src.utils.config import config
        
        # Test critical config values
        tests = [
            ('min_profit', config.min_profit, float),
            ('trading_fee', config.trading_fee, float),
            ('gas_estimate', config.gas_estimate, float),
            ('demo_balance', config.demo_balance, float),
            ('auto_execute', config.auto_execute, bool)
        ]
        
        for name, value, expected_type in tests:
            if isinstance(value, expected_type):
                print(f"  ✓ {name}: {value}")
            else:
                print(f"  ✗ {name}: {value} (wrong type, expected {expected_type.__name__})")
                return False
        
        return True
    except Exception as e:
        print(f"  ✗ Configuration error: {e}")
        return False

def validate_core_logic():
    """Validate core trading logic"""
    print("\n🧠 Validating core logic...")
    
    try:
        # Test arbitrage detection
        from src.core.arbitrage import ArbitrageDetector
        detector = ArbitrageDetector()
        
        # Should find opportunity
        opp = detector.check_arbitrage("test", "Test", 0.45, 0.50)
        if opp and opp.estimated_profit > 0:
            print(f"  ✓ Arbitrage detection: ${opp.estimated_profit:.4f} profit")
        else:
            print("  ✗ Arbitrage detection failed")
            return False
        
        # Test demo mode
        from src.core.demo_mode import DemoMode
        demo = DemoMode(1000.0)
        trade = demo.execute_arbitrage("Test", 0.45, 0.50)
        
        if trade.profit > 0 and demo.balance > 1000.0:
            print(f"  ✓ Demo mode: ${trade.profit:.4f} profit")
        else:
            print("  ✗ Demo mode failed")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Core logic error: {e}")
        return False

async def validate_api():
    """Validate API connectivity"""
    print("\n🌐 Validating API connectivity...")
    
    try:
        from src.core.market import PolymarketAPI
        
        api = PolymarketAPI()
        markets = await api.fetch_markets(limit=2)
        await api.close()
        
        if len(markets) > 0:
            print(f"  ✓ Polymarket API: {len(markets)} markets fetched")
            print(f"    Example: {markets[0].question[:40]}...")
            return True
        else:
            print("  ✗ Polymarket API: No markets returned")
            return False
    except Exception as e:
        print(f"  ✗ Polymarket API error: {e}")
        return False

def validate_imports():
    """Validate all imports work correctly"""
    print("\n📦 Validating imports...")
    
    imports = [
        ('src.utils.config', 'Configuration loader'),
        ('src.utils.logger', 'Logging system'),
        ('src.core.arbitrage', 'Arbitrage detection'),
        ('src.core.demo_mode', 'Demo trading mode'),
        ('src.core.market', 'Market data and API'),
    ]
    
    for module, description in imports:
        try:
            __import__(module)
            print(f"  ✓ {module} - {description}")
        except ImportError as e:
            print(f"  ✗ {module} - {description} - {e}")
            return False
    
    # GUI import (may fail in headless)
    try:
        __import__('src.gui.main_window')
        print("  ✓ src.gui.main_window - GUI components")
    except ImportError as e:
        if 'libEGL' in str(e) or 'display' in str(e):
            print("  ⚠ src.gui.main_window - GUI components (headless mode)")
        else:
            print(f"  ✗ src.gui.main_window - GUI components - {e}")
            return False
    
    return True

async def main():
    """Run all validation tests"""
    print("🚀 Polymarket Arbitrage Bot - Installation Validator")
    print("=" * 60)
    
    validators = [
        ("Dependencies", validate_dependencies),
        ("File Structure", validate_files),
        ("Configuration", validate_config),
        ("Core Logic", validate_core_logic),
        ("Imports", validate_imports),
        ("API Connectivity", validate_api),
    ]
    
    passed = 0
    total = len(validators)
    
    for name, validator in validators:
        try:
            if asyncio.iscoroutinefunction(validator):
                result = await validator()
            else:
                result = validator()
            
            if result:
                passed += 1
                print(f"✅ {name} validation passed")
            else:
                print(f"❌ {name} validation failed")
        except Exception as e:
            print(f"❌ {name} validation error: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Validation Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 SUCCESS: Installation is valid and ready!")
        print("\nTo run the bot:")
        print("  Windows: Double-click launcher.bat")
        print("  Linux/Mac: ./launcher.sh")
        return True
    else:
        print("\n❌ FAILED: Installation has issues that need to be fixed")
        print("\nPlease:")
        print("  1. Run the installer again")
        print("  2. Check that all dependencies are installed")
        print("  3. Verify internet connectivity for API tests")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)