"""
Stock Alert Automation System - Main Application
Continuously monitors Yes Bank stock price and sends email alerts
"""
import logging
import schedule
import time
import signal
import sys
from datetime import datetime
from config import Config
from email_service import EmailService
from stock_monitor import StockMonitor

class StockAlertSystem:
    """Main application class for stock alert system"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.running = True
        
        # Initialize services
        self.email_service = EmailService()
        self.stock_monitor = StockMonitor(self.email_service)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def setup_logging(self):
        """Configure logging system"""
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format=Config.LOG_FORMAT,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('stock_alert.log', mode='a', encoding='utf-8')
            ]
        )
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}. Shutting down gracefully...")
        self.running = False
    
    def validate_configuration(self):
        """Validate all configuration and connections"""
        self.logger.info("Validating system configuration...")
        
        try:
            # Validate config
            Config.validate_config()
            self.logger.info("[OK] Configuration validation passed")
            
            # Test email connection
            if not self.email_service.test_connection():
                raise Exception("Email service connection failed")
            self.logger.info("[OK] Email service connection successful")
            
            # Test Yahoo Finance connection
            if not self.stock_monitor.test_connection():
                raise Exception("Yahoo Finance connection failed")
            self.logger.info("[OK] Yahoo Finance connection successful")
            
            return True
            
        except Exception as e:
            self.logger.error(f"[FAIL] Configuration validation failed: {str(e)}")
            return False
    
    def run_price_check(self):
        """Scheduled function to check stock price with market hours awareness"""
        try:
            self.logger.debug("Running scheduled price check...")
            success = self.stock_monitor.monitor_price()
            
            if not success:
                self.logger.warning("Price check completed with warnings")
            
            # Log market status and price statistics every 10 checks (10 minutes)
            if hasattr(self, 'check_count'):
                self.check_count += 1
            else:
                self.check_count = 1
                
            if self.check_count % 10 == 0:
                # Log market status
                market_status = self.stock_monitor.get_market_status()
                status_msg = "OPEN" if market_status['is_open'] else "CLOSED"
                self.logger.info(f"Market Status: {status_msg} at {market_status['current_time_ist']}")
                
                # Log price statistics
                stats = self.stock_monitor.get_price_statistics()
                if stats:
                    self.logger.info(f"Price stats (last {stats['data_points']} checks): "
                                   f"Current: ₹{stats['current_price']:.2f}, "
                                   f"Min: ₹{stats['min_price']:.2f}, "
                                   f"Max: ₹{stats['max_price']:.2f}, "
                                   f"Avg: ₹{stats['avg_price']:.2f}")
                
                # Log alert status
                alert_status = "READY" if not self.stock_monitor.alert_sent else "SENT (waiting for price recovery)"
                self.logger.info(f"Alert Status: {alert_status}")
                    
        except Exception as e:
            self.logger.error(f"Error in scheduled price check: {str(e)}")
    
    def start_monitoring(self):
        """Start the main monitoring loop"""
        self.logger.info("🚀 Starting Enhanced Stock Alert Automation System")
        self.logger.info(f"Monitoring: {Config.STOCK_SYMBOL}")
        self.logger.info(f"Threshold: ₹{Config.PRICE_THRESHOLD}")
        self.logger.info(f"Check interval: {Config.CHECK_INTERVAL} seconds")
        self.logger.info(f"Market hours: {Config.MARKET_OPEN_TIME.strftime('%H:%M')} - {Config.MARKET_CLOSE_TIME.strftime('%H:%M')} IST")
        self.logger.info("Alert logic: Only during market hours, rate-limited per threshold crossing")
        
        # Validate system before starting
        if not self.validate_configuration():
            self.logger.error("System validation failed. Exiting...")
            return False
        
        # Show initial market status
        market_status = self.stock_monitor.get_market_status()
        if market_status['is_open']:
            self.logger.info(f"🟢 Market is currently OPEN (closes in {market_status['time_to_close']})")
        else:
            self.logger.info(f"🔴 Market is currently CLOSED (opens in {market_status['time_to_open']})")
        
        # Schedule price checks
        schedule.every(Config.CHECK_INTERVAL).seconds.do(self.run_price_check)
        
        # Run initial price check
        self.logger.info("Running initial price check...")
        self.run_price_check()
        
        # Main monitoring loop
        self.logger.info("✅ System started successfully. Monitoring in progress...")
        
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)  # Small sleep to prevent high CPU usage
                
        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt")
        except Exception as e:
            self.logger.error(f"Unexpected error in main loop: {str(e)}")
        
        self.logger.info("🛑 Stock Alert System stopped")
        return True
    
    def run_system_test(self):
        """Run comprehensive system test"""
        self.logger.info("🧪 Running enhanced system test...")
        
        # Test configuration
        if not self.validate_configuration():
            return False
        
        # Show market status
        market_status = self.stock_monitor.get_market_status()
        if market_status['is_open']:
            self.logger.info(f"🟢 Market Status: OPEN (closes in {market_status['time_to_close']})")
        else:
            self.logger.info(f"🔴 Market Status: CLOSED (opens in {market_status['time_to_open']})")
        
        # Test price fetching
        current_price = self.stock_monitor.get_current_price()
        if current_price is None:
            # Check if market is closed - this is acceptable
            market_status = self.stock_monitor.get_market_status()
            if not market_status['is_open']:
                self.logger.warning("⚠️ Price fetching failed but market is closed - this is normal")
                self.logger.info("✅ System will fetch prices when market opens")
            else:
                self.logger.error("❌ Price fetching test failed during market hours")
                return False
        else:
            self.logger.info(f"✅ Current price fetched: ₹{current_price:.2f}")
        
        # Test alert logic (only send test email if specifically requested and market is open)
        if market_status['is_open'] and current_price and current_price < Config.PRICE_THRESHOLD:
            self.logger.info("⚠️ Price is below threshold and market is open. Testing email alert...")
            test_result = self.email_service.send_alert(current_price)
            if test_result:
                self.logger.info("✅ Test email sent successfully")
            else:
                self.logger.error("❌ Test email failed")
                return False
        else:
            if not market_status['is_open']:
                reason = "market closed"
            elif not current_price:
                reason = "price data unavailable"
            else:
                reason = f"price ₹{current_price:.2f} above threshold ₹{Config.PRICE_THRESHOLD}"
            self.logger.info(f"ℹ️ Skipping email test - {reason}")
        
        # Test alert state logic
        self.logger.info(f"Alert state: {'SENT' if self.stock_monitor.alert_sent else 'READY'}")
        self.logger.info(f"Last price above threshold: {self.stock_monitor.last_price_above_threshold}")
        
        self.logger.info("🎉 All system tests passed!")
        return True

def main():
    """Main entry point"""
    try:
        # Create and start the stock alert system
        system = StockAlertSystem()
        
        # Check if this is a test run
        if len(sys.argv) > 1 and sys.argv[1] == '--test':
            return system.run_system_test()
        else:
            return system.start_monitoring()
            
    except Exception as e:
        logging.error(f"Critical error in main: {str(e)}")
        return False

if __name__ == "__main__":
    main()
