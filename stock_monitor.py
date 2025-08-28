"""
Stock monitoring service for tracking Yes Bank price
Handles price fetching, threshold monitoring, and alert triggering with market hours support
"""
import yfinance as yf
import logging
import time
from datetime import datetime, timedelta
from config import Config

class StockMonitor:
    """Monitors stock price and manages alert logic with market hours awareness"""
    
    def __init__(self, email_service):
        self.logger = logging.getLogger(__name__)
        self.email_service = email_service
        self.stock_symbol = Config.STOCK_SYMBOL
        self.threshold = Config.PRICE_THRESHOLD
        
        # Alert state management for proper rate limiting
        self.alert_sent = False  # Track if alert was sent for current below-threshold period
        self.last_price_above_threshold = True  # Track if last price was above threshold
        self.price_history = []  # Store recent prices for analysis
        
        # Create yfinance ticker object
        self.ticker = yf.Ticker(self.stock_symbol)
        
    def is_market_open(self):
        """Check if market is currently open"""
        return Config.is_market_open()
    
    def get_current_price(self):
        """
        Fetch current stock price from Yahoo Finance with real-time data
        
        Returns:
            float: Current stock price, None if failed
        """
        try:
            # For real-time data during market hours, use 1-minute interval
            if self.is_market_open():
                # Get most recent 1-minute data for real-time prices
                data = self.ticker.history(period="1d", interval="1m")
                
                if data.empty:
                    self.logger.warning("No real-time data available, trying intraday data...")
                    # Fallback to regular daily data
                    data = self.ticker.history(period="1d")
            else:
                # Outside market hours, get the latest closing price from the last trading day
                data = self.ticker.history(period="5d")
                if not data.empty:
                    self.logger.info("Market closed - using last trading day's closing price")
                
            if data.empty:
                self.logger.warning("No price data available from Yahoo Finance")
                return None
            
            # Get the latest available price
            current_price = float(data['Close'].iloc[-1])
            data_timestamp = data.index[-1].strftime("%Y-%m-%d %H:%M:%S")
            
            # Store price in history (keep last 100 entries)
            self.price_history.append({
                'price': current_price,
                'timestamp': datetime.now(),
                'data_timestamp': data_timestamp
            })
            
            # Keep only last 100 price points
            if len(self.price_history) > 100:
                self.price_history = self.price_history[-100:]
            
            # Log with market status
            market_status = "OPEN" if self.is_market_open() else "CLOSED"
            self.logger.info(f"[{market_status}] {self.stock_symbol} price: ₹{current_price:.2f} (data from: {data_timestamp})")
            return current_price
            
        except Exception as e:
            self.logger.error(f"Error fetching stock price: {str(e)}")
            return None
    
    def should_send_alert(self, current_price):
        """
        Enhanced alert logic: only send alert during market hours when price drops below threshold
        and we haven't already sent an alert for this below-threshold period
        
        Args:
            current_price (float): Current stock price
            
        Returns:
            bool: True if alert should be sent, False otherwise
        """
        # First check: Market must be open
        if not self.is_market_open():
            self.logger.debug("Market is closed - no alerts will be sent")
            return False
        
        # Second check: Price must be below threshold
        if current_price >= self.threshold:
            # Price is above threshold - reset alert state for next time
            if not self.last_price_above_threshold:
                self.logger.info(f"Price recovered above threshold ₹{self.threshold}. Ready for next alert.")
                self.alert_sent = False  # Reset alert state
            self.last_price_above_threshold = True
            return False
        
        # Price is below threshold
        self.last_price_above_threshold = False
        
        # Third check: Have we already sent an alert for this below-threshold period?
        if self.alert_sent:
            self.logger.debug(f"Alert already sent for current below-threshold period. Price: ₹{current_price:.2f}")
            return False
        
        # All conditions met - send alert
        self.logger.warning(f"Alert conditions met: Market open, price ₹{current_price:.2f} below ₹{self.threshold}, no recent alert")
        return True
    
    def send_price_alert(self, current_price):
        """
        Send price alert and update alert state
        
        Args:
            current_price (float): Current stock price
            
        Returns:
            bool: True if alert sent successfully, False otherwise
        """
        # Format timestamp in IST
        ist_time = datetime.now(Config.MARKET_TIMEZONE)
        timestamp = ist_time.strftime("%Y-%m-%d %H:%M:%S IST")
        
        # Send email alert
        if self.email_service.send_alert(current_price, timestamp):
            self.alert_sent = True  # Mark that we've sent an alert for this period
            self.logger.info(f"✅ Price alert sent for ₹{current_price:.2f} at {timestamp}")
            return True
        else:
            self.logger.error("❌ Failed to send price alert")
            return False
    
    def monitor_price(self):
        """
        Main monitoring function with market hours awareness
        
        Returns:
            bool: True if monitoring completed successfully, False if failed
        """
        try:
            # Check market status first
            market_open = self.is_market_open()
            
            # Get current price
            current_price = self.get_current_price()
            
            if current_price is None:
                self.logger.warning("Unable to fetch current price")
                return False
            
            if not market_open:
                self.logger.debug(f"Market closed. Current price: ₹{current_price:.2f} (monitoring only)")
                return True
            
            # Market is open - check for alerts
            if self.should_send_alert(current_price):
                return self.send_price_alert(current_price)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in price monitoring: {str(e)}")
            return False
    
    def get_market_status(self):
        """Get detailed market status information"""
        ist_now = datetime.now(Config.MARKET_TIMEZONE)
        market_open = self.is_market_open()
        
        status = {
            'is_open': market_open,
            'current_time_ist': ist_now.strftime("%Y-%m-%d %H:%M:%S IST"),
            'current_weekday': ist_now.strftime("%A"),
            'market_open_time': Config.MARKET_OPEN_TIME.strftime("%H:%M"),
            'market_close_time': Config.MARKET_CLOSE_TIME.strftime("%H:%M")
        }
        
        if market_open:
            # Calculate time until market close
            market_close_today = ist_now.replace(
                hour=Config.MARKET_CLOSE_TIME.hour,
                minute=Config.MARKET_CLOSE_TIME.minute,
                second=0,
                microsecond=0
            )
            time_to_close = market_close_today - ist_now
            status['time_to_close'] = str(time_to_close).split('.')[0]  # Remove microseconds
        else:
            # Calculate time until next market open
            if ist_now.weekday() >= 5:  # Weekend
                # Next Monday
                days_until_monday = 7 - ist_now.weekday()
                next_open = ist_now.replace(
                    hour=Config.MARKET_OPEN_TIME.hour,
                    minute=Config.MARKET_OPEN_TIME.minute,
                    second=0,
                    microsecond=0
                ) + timedelta(days=days_until_monday)
            else:
                # Check if today's market has closed or not yet opened
                market_open_today = ist_now.replace(
                    hour=Config.MARKET_OPEN_TIME.hour,
                    minute=Config.MARKET_OPEN_TIME.minute,
                    second=0,
                    microsecond=0
                )
                
                if ist_now.time() < Config.MARKET_OPEN_TIME:
                    # Market hasn't opened today
                    next_open = market_open_today
                else:
                    # Market has closed today, next open is tomorrow
                    next_open = market_open_today + timedelta(days=1)
            
            time_to_open = next_open - ist_now
            status['time_to_open'] = str(time_to_open).split('.')[0]  # Remove microseconds
        
        return status
    
    def get_price_statistics(self):
        """Get basic statistics about recent price history"""
        if not self.price_history:
            return None
        
        prices = [entry['price'] for entry in self.price_history]
        return {
            'current_price': prices[-1] if prices else None,
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': sum(prices) / len(prices),
            'data_points': len(prices),
            'time_span_minutes': len(prices)
        }
    
    def test_connection(self):
        """Test connection to Yahoo Finance and show market status"""
        try:
            # Test price fetching
            test_price = self.get_current_price()
            if test_price is not None:
                self.logger.info(f"Yahoo Finance connection successful. Current price: ₹{test_price:.2f}")
                
                # Show market status
                market_status = self.get_market_status()
                if market_status['is_open']:
                    self.logger.info(f"✅ Market is OPEN (closes in {market_status['time_to_close']})")
                else:
                    self.logger.info(f"🔒 Market is CLOSED (opens in {market_status['time_to_open']})")
                
                return True
            else:
                self.logger.warning("Yahoo Finance connection issues detected (common outside market hours)")
                # Show market status even when connection fails
                market_status = self.get_market_status()
                if market_status['is_open']:
                    self.logger.warning("⚠️ Market is OPEN but data unavailable - will retry during monitoring")
                    return False  # Fail if market is open but no data
                else:
                    self.logger.info(f"🔒 Market is CLOSED (opens in {market_status['time_to_open']}) - connection issues are normal")
                    return True  # Accept connection issues when market is closed
        except Exception as e:
            self.logger.error(f"Yahoo Finance connection test error: {str(e)}")
            # Check market status to determine if this is critical
            market_status = self.get_market_status()
            if market_status['is_open']:
                self.logger.error("❌ Connection failed during market hours - this needs attention")
                return False
            else:
                self.logger.warning("⚠️ Connection failed outside market hours - will retry when market opens")
                return True
