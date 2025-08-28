"""
Configuration management for Stock Alert System
Handles environment variables and application settings
"""
import os
from dotenv import load_dotenv
import pytz
from datetime import time

# Load environment variables from .env file (for local development)
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Stock Configuration
    STOCK_SYMBOL = "YESBANK.NS"  # Yes Bank NSE listing
    PRICE_THRESHOLD = 18.00      # Alert when price drops below this value (updated threshold)
    CHECK_INTERVAL = 60          # Check price every 60 seconds
    
    # Market Hours Configuration (NSE Trading Hours)
    MARKET_TIMEZONE = pytz.timezone('Asia/Kolkata')
    MARKET_OPEN_TIME = time(9, 15)   # 09:15 AM IST
    MARKET_CLOSE_TIME = time(15, 30) # 03:30 PM IST
    
    # Email Configuration
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "baveshchowdary1@gmail.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "ilsp zgmj pfhj iyli")
    
    # Notification Settings
    ALERT_SUBJECT = "YES Bank Stock Alert"
    
    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    
    # Retry Configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
    
    @classmethod
    def get_alert_body(cls, current_price, timestamp):
        """Generate email alert body"""
        return f"""YES Bank price is ₹{current_price:.2f}, crossed your threshold ₹{cls.PRICE_THRESHOLD}.

Alert Details:
- Stock Symbol: {cls.STOCK_SYMBOL}
- Current Price: ₹{current_price:.2f}
- Threshold: ₹{cls.PRICE_THRESHOLD}
- Alert Time: {timestamp}

This alert was triggered during NSE market hours (09:15 AM - 03:30 PM IST).
"""
    
    @classmethod
    def is_market_open(cls):
        """
        Check if NSE market is currently open
        
        Returns:
            bool: True if market is open, False otherwise
        """
        from datetime import datetime
        
        # Get current IST time
        ist_now = datetime.now(cls.MARKET_TIMEZONE)
        current_time = ist_now.time()
        current_weekday = ist_now.weekday()  # 0=Monday, 6=Sunday
        
        # Check if it's a weekday (Monday=0 to Friday=4)
        if current_weekday > 4:  # Saturday=5, Sunday=6
            return False
        
        # Check if current time is within market hours
        return cls.MARKET_OPEN_TIME <= current_time <= cls.MARKET_CLOSE_TIME

    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        required_vars = [
            ('EMAIL_ADDRESS', cls.EMAIL_ADDRESS),
            ('EMAIL_PASSWORD', cls.EMAIL_PASSWORD)
        ]
        
        missing_vars = []
        for var_name, var_value in required_vars:
            if not var_value or var_value == "":
                missing_vars.append(var_name)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
