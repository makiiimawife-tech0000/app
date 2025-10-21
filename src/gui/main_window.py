"""Main GUI window"""
import sys
import asyncio
from typing import Optional, List
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QRadioButton,
    QButtonGroup, QGroupBox, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor

from ..core.market import Market, MarketDataFetcher
from ..core.arbitrage import ArbitrageDetector, ArbitrageOpportunity
from ..core.demo_mode import DemoMode
from ..utils.config import config
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class MarketFetchThread(QThread):
    """Thread for fetching markets asynchronously"""
    markets_fetched = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, fetcher: MarketDataFetcher):
        super().__init__()
        self.fetcher = fetcher
    
    def run(self):
        """Fetch markets in background"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            markets = loop.run_until_complete(self.fetcher.fetch_markets(limit=50))
            loop.close()
            
            self.markets_fetched.emit(markets)
        except Exception as e:
            self.error_occurred.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.markets: List[Market] = []
        self.selected_market: Optional[Market] = None
        self.fetcher = MarketDataFetcher()
        self.detector = ArbitrageDetector(
            min_profit=config.min_profit,
            trading_fee=config.trading_fee,
            gas_cost=config.gas_estimate
        )
        self.demo_mode = DemoMode(initial_balance=config.demo_balance)
        
        # Monitoring state
        self.monitoring = False
        self.current_mode = "demo"
        
        # Setup UI
        self.init_ui()
        
        # Fetch markets on startup
        self.fetch_markets()
        
        # Setup price simulation timer (for demo)
        self.price_timer = QTimer()
        self.price_timer.timeout.connect(self.simulate_price_update)
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(config.get('app.name', 'Polymarket Arbitrage Tool'))
        self.setGeometry(100, 100, config.get('app.window_width', 900), config.get('app.window_height', 700))
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("Polymarket Arbitrage Tool")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Mode selection
        mode_group = self.create_mode_selection()
        main_layout.addWidget(mode_group)
        
        # Market selection
        market_group = self.create_market_selection()
        main_layout.addWidget(market_group)
        
        # Price display
        price_group = self.create_price_display()
        main_layout.addWidget(price_group)
        
        # Controls
        controls_layout = self.create_controls()
        main_layout.addLayout(controls_layout)
        
        # Log output
        log_group = self.create_log_display()
        main_layout.addWidget(log_group)
        
        # Status bar
        status_layout = self.create_status_bar()
        main_layout.addLayout(status_layout)
    
    def create_mode_selection(self) -> QGroupBox:
        """Create mode selection group"""
        group = QGroupBox("Trading Mode")
        layout = QHBoxLayout()
        
        self.demo_radio = QRadioButton("Demo Mode (Fake Money)")
        self.demo_radio.setChecked(True)
        self.demo_radio.toggled.connect(self.on_mode_changed)
        
        self.real_radio = QRadioButton("Real Mode (Your Account)")
        self.real_radio.setEnabled(False)  # Enable in Phase 2
        
        layout.addWidget(self.demo_radio)
        layout.addWidget(self.real_radio)
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    def create_market_selection(self) -> QGroupBox:
        """Create market selection group"""
        group = QGroupBox("Market Selection")
        layout = QVBoxLayout()
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to search markets...")
        self.search_input.textChanged.connect(self.on_search_changed)
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.fetch_markets)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(search_layout)
        
        # Market list
        self.market_list = QListWidget()
        self.market_list.itemClicked.connect(self.on_market_selected)
        layout.addWidget(self.market_list)
        
        group.setLayout(layout)
        return group
    
    def create_price_display(self) -> QGroupBox:
        """Create price display group"""
        group = QGroupBox("Current Prices")
        layout = QVBoxLayout()
        
        # Selected market name
        self.market_name_label = QLabel("No market selected")
        self.market_name_label.setWordWrap(True)
        layout.addWidget(self.market_name_label)
        
        # Prices
        price_layout = QHBoxLayout()
        
        self.yes_price_label = QLabel("YES: $--.--")
        self.yes_price_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        
        self.no_price_label = QLabel("NO: $--.--")
        self.no_price_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        
        self.total_label = QLabel("Total: $--.--")
        self.total_label.setStyleSheet("font-size: 14pt;")
        
        price_layout.addWidget(self.yes_price_label)
        price_layout.addWidget(self.no_price_label)
        price_layout.addWidget(self.total_label)
        price_layout.addStretch()
        
        layout.addLayout(price_layout)
        
        # Arbitrage alert
        self.arb_alert = QLabel("")
        self.arb_alert.setStyleSheet(
            "font-size: 12pt; font-weight: bold; color: green; padding: 10px;"
        )
        layout.addWidget(self.arb_alert)
        
        group.setLayout(layout)
        return group
    
    def create_controls(self) -> QHBoxLayout:
        """Create control buttons"""
        layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ Start Monitoring")
        self.start_btn.clicked.connect(self.start_monitoring)
        self.start_btn.setEnabled(False)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.stop_btn.setEnabled(False)
        
        self.execute_btn = QPushButton("⚡ Execute Once")
        self.execute_btn.clicked.connect(self.execute_once)
        self.execute_btn.setEnabled(False)
        
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.execute_btn)
        layout.addStretch()
        
        return layout
    
    def create_log_display(self) -> QGroupBox:
        """Create log display group"""
        group = QGroupBox("Activity Log")
        layout = QVBoxLayout()
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(200)
        
        layout.addWidget(self.log_output)
        group.setLayout(layout)
        return group
    
    def create_status_bar(self) -> QHBoxLayout:
        """Create status bar"""
        layout = QHBoxLayout()
        
        self.balance_label = QLabel(f"Balance: ${self.demo_mode.balance:.2f} (demo)")
        self.profit_label = QLabel(f"Total Profit: ${self.demo_mode.total_profit:.2f}")
        self.trades_label = QLabel(f"Trades: {self.demo_mode.num_trades}")
        
        layout.addWidget(self.balance_label)
        layout.addWidget(self.profit_label)
        layout.addWidget(self.trades_label)
        layout.addStretch()
        
        return layout
    
    def fetch_markets(self):
        """Fetch markets from Polymarket"""
        self.log("Fetching markets from Polymarket...")
        self.refresh_btn.setEnabled(False)
        
        self.fetch_thread = MarketFetchThread(self.fetcher)
        self.fetch_thread.markets_fetched.connect(self.on_markets_fetched)
        self.fetch_thread.error_occurred.connect(self.on_fetch_error)
        self.fetch_thread.start()
    
    def on_markets_fetched(self, markets: List[Market]):
        """Handle markets fetched"""
        self.markets = markets
        self.update_market_list(markets)
        self.log(f"Loaded {len(markets)} markets")
        self.refresh_btn.setEnabled(True)
    
    def on_fetch_error(self, error: str):
        """Handle fetch error"""
        self.log(f"Error fetching markets: {error}")
        self.refresh_btn.setEnabled(True)
        QMessageBox.warning(self, "Error", f"Failed to fetch markets: {error}")
    
    def update_market_list(self, markets: List[Market]):
        """Update market list widget"""
        self.market_list.clear()
        for market in markets:
            item = QListWidgetItem(market.question)
            item.setData(Qt.ItemDataRole.UserRole, market)
            self.market_list.addItem(item)
    
    def on_search_changed(self, text: str):
        """Handle search text changed"""
        if not text:
            self.update_market_list(self.markets)
        else:
            filtered = [m for m in self.markets if text.lower() in m.question.lower()]
            self.update_market_list(filtered)
    
    def on_market_selected(self, item: QListWidgetItem):
        """Handle market selection"""
        self.selected_market = item.data(Qt.ItemDataRole.UserRole)
        self.market_name_label.setText(f"Selected: {self.selected_market.question}")
        self.start_btn.setEnabled(True)
        self.execute_btn.setEnabled(False)
        self.log(f"Selected market: {self.selected_market.question}")
        
        # Reset prices
        self.yes_price_label.setText("YES: $--.--")
        self.no_price_label.setText("NO: $--.--")
        self.total_label.setText("Total: $--.--")
        self.arb_alert.setText("")
    
    def on_mode_changed(self):
        """Handle mode change"""
        self.current_mode = "demo" if self.demo_radio.isChecked() else "real"
        self.log(f"Switched to {self.current_mode.upper()} mode")
        self.update_status()
    
    def start_monitoring(self):
        """Start monitoring selected market"""
        if not self.selected_market:
            return
        
        self.monitoring = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.execute_btn.setEnabled(True)
        
        self.log(f"Started monitoring: {self.selected_market.question}")
        
        # Start price simulation (in real version, connect to WebSocket)
        self.price_timer.start(500)  # Update every 500ms
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.execute_btn.setEnabled(False)
        
        self.price_timer.stop()
        self.log("Stopped monitoring")
    
    def simulate_price_update(self):
        """Simulate price updates (replace with WebSocket in production)"""
        import random
        
        if not self.monitoring or not self.selected_market:
            return
        
        # Generate random prices that occasionally create arbitrage
        # In production, these come from WebSocket
        base = random.uniform(0.40, 0.60)
        spread = random.uniform(0.01, 0.15)
        
        yes_price = base
        no_price = 1.0 - base + spread * random.choice([-1, 1])
        
        # Clamp prices
        yes_price = max(0.01, min(0.99, yes_price))
        no_price = max(0.01, min(0.99, no_price))
        
        self.update_prices(yes_price, no_price)
    
    def update_prices(self, yes_price: float, no_price: float):
        """Update displayed prices and check for arbitrage"""
        # Update labels
        self.yes_price_label.setText(f"YES: ${yes_price:.2f}")
        self.no_price_label.setText(f"NO: ${no_price:.2f}")
        
        total = yes_price + no_price
        self.total_label.setText(f"Total: ${total:.2f}")
        
        # Check for arbitrage
        if self.selected_market:
            opp = self.detector.check_arbitrage(
                self.selected_market.id,
                self.selected_market.question,
                yes_price,
                no_price
            )
            
            if opp:
                # Show arbitrage alert
                alert_text = f"⚠️ ARBITRAGE! Profit: ${opp.estimated_profit:.4f} ({opp.profit_percentage:.2f}%)"
                self.arb_alert.setText(alert_text)
                self.arb_alert.setStyleSheet(
                    "font-size: 12pt; font-weight: bold; color: green; "
                    "background-color: #d4edda; padding: 10px; border-radius: 5px;"
                )
                
                # Auto-execute if enabled
                if config.auto_execute and self.current_mode == "demo":
                    self.execute_arbitrage(opp)
            else:
                self.arb_alert.setText("")
    
    def execute_once(self):
        """Execute arbitrage once manually"""
        if not self.selected_market:
            return
        
        # Get current prices from labels
        yes_text = self.yes_price_label.text().split('$')[1]
        no_text = self.no_price_label.text().split('$')[1]
        
        try:
            yes_price = float(yes_text)
            no_price = float(no_text)
        except:
            self.log("No valid prices to execute")
            return
        
        # Check for arbitrage
        opp = self.detector.check_arbitrage(
            self.selected_market.id,
            self.selected_market.question,
            yes_price,
            no_price
        )
        
        if opp:
            self.execute_arbitrage(opp)
        else:
            self.log("No arbitrage opportunity at current prices")
    
    def execute_arbitrage(self, opp: ArbitrageOpportunity):
        """Execute the arbitrage trade"""
        if self.current_mode == "demo":
            # Execute in demo mode
            trade = self.demo_mode.execute_arbitrage(
                market_name=opp.market_name,
                yes_price=opp.yes_price,
                no_price=opp.no_price,
                trading_fee=self.detector.trading_fee,
                gas_cost=self.detector.gas_cost
            )
            
            # Log the trade
            self.log(str(trade))
            self.log(f"[DEMO] Balance: ${self.demo_mode.balance:.2f}, Total Profit: ${self.demo_mode.total_profit:.2f}")
            
            # Update status
            self.update_status()
            
            # Clear arbitrage alert
            self.arb_alert.setText("")
        else:
            # Real mode (Phase 2)
            self.log("[REAL MODE] Not implemented yet")
    
    def update_status(self):
        """Update status bar"""
        mode_text = "demo" if self.current_mode == "demo" else "real"
        self.balance_label.setText(f"Balance: ${self.demo_mode.balance:.2f} ({mode_text})")
        self.profit_label.setText(f"Total Profit: ${self.demo_mode.total_profit:.2f}")
        self.trades_label.setText(f"Trades: {self.demo_mode.num_trades}")
    
    def log(self, message: str):
        """Add message to log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{timestamp}] {message}")
        logger.info(message)
    
    def closeEvent(self, event):
        """Handle window close"""
        self.price_timer.stop()
        event.accept()


def run_gui():
    """Run the GUI application"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
