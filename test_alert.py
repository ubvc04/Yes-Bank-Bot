"""
Demo script to test email alert functionality
Temporarily sets a high threshold to trigger an alert
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from email_service import EmailService
from stock_monitor import StockMonitor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_alert_functionality():
    """Test the alert system with mock data"""
    print("=== TESTING ALERT FUNCTIONALITY ===")
    
    # Initialize services
    email_service = EmailService()
    stock_monitor = StockMonitor(email_service)
    
    # Get current mock price
    current_price = stock_monitor.get_current_price()
    print(f"Current price: Rs.{current_price:.2f}")
    
    # Test alert with a price below threshold
    test_price = 17.50  # Below the 17.99 threshold
    print(f"\nTesting alert with price Rs.{test_price:.2f} (below threshold Rs.{Config.PRICE_THRESHOLD})")
    
    # Send test alert
    result = email_service.send_alert(test_price)
    if result:
        print("✓ TEST EMAIL SENT SUCCESSFULLY!")
        print(f"Check your email: {Config.EMAIL_ADDRESS}")
    else:
        print("✗ Email sending failed")
    
    return result

if __name__ == "__main__":
    test_alert_functionality()
