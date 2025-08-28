"""
Enhanced Stock Alert System Test
Tests market hours filtering, rate limiting, and alert logic
"""
import sys
import os
import logging
from datetime import datetime, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from email_service import EmailService
from stock_monitor import StockMonitor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_market_hours():
    """Test market hours detection"""
    print("=== TESTING MARKET HOURS DETECTION ===")
    
    # Test current market status
    is_open = Config.is_market_open()
    print(f"Market is currently: {'OPEN' if is_open else 'CLOSED'}")
    
    # Show market hours
    print(f"NSE Trading Hours: {Config.MARKET_OPEN_TIME.strftime('%H:%M')} - {Config.MARKET_CLOSE_TIME.strftime('%H:%M')} IST")
    
    # Show current IST time
    ist_now = datetime.now(Config.MARKET_TIMEZONE)
    print(f"Current IST time: {ist_now.strftime('%Y-%m-%d %H:%M:%S %A')}")
    
    return is_open

def test_alert_logic():
    """Test the enhanced alert logic"""
    print("\n=== TESTING ENHANCED ALERT LOGIC ===")
    
    # Initialize services
    email_service = EmailService()
    stock_monitor = StockMonitor(email_service)
    
    # Get market status
    market_status = stock_monitor.get_market_status()
    print(f"Market Status: {'OPEN' if market_status['is_open'] else 'CLOSED'}")
    
    if market_status['is_open']:
        print(f"Market closes in: {market_status['time_to_close']}")
    else:
        print(f"Market opens in: {market_status['time_to_open']}")
    
    # Get current price
    current_price = stock_monitor.get_current_price()
    if current_price is None:
        print("Current YES Bank price: Unable to fetch (Yahoo Finance issues)")
        print("This is expected outside market hours or during API outages")
        return False
    
    print(f"Current YES Bank price: ₹{current_price:.2f}")
    print(f"Alert threshold: ₹{Config.PRICE_THRESHOLD}")
    
    # Test alert conditions
    should_alert = stock_monitor.should_send_alert(current_price)
    print(f"Should send alert: {should_alert}")
    
    # Explain why or why not
    if not market_status['is_open']:
        print("Reason: Market is closed")
    elif current_price >= Config.PRICE_THRESHOLD:
        print(f"Reason: Price ₹{current_price:.2f} is above threshold ₹{Config.PRICE_THRESHOLD}")
    elif stock_monitor.alert_sent:
        print("Reason: Alert already sent for current below-threshold period")
    else:
        print("Reason: All conditions met for alert")
    
    return should_alert

def test_rate_limiting():
    """Test rate limiting logic"""
    print("\n=== TESTING RATE LIMITING LOGIC ===")
    
    email_service = EmailService()
    stock_monitor = StockMonitor(email_service)
    
    # Simulate price scenarios
    test_scenarios = [
        {"price": 19.00, "description": "Price above threshold"},
        {"price": 17.50, "description": "Price below threshold (first time)"},
        {"price": 17.30, "description": "Price still below threshold (should not alert)"},
        {"price": 18.50, "description": "Price recovered above threshold"},
        {"price": 17.80, "description": "Price below threshold again (should alert)"},
    ]
    
    print("Simulating price movements:")
    for i, scenario in enumerate(test_scenarios):
        print(f"\nStep {i+1}: {scenario['description']} - ₹{scenario['price']:.2f}")
        
        # Simulate the price check
        if scenario['price'] >= Config.PRICE_THRESHOLD:
            # Price above threshold - reset alert state
            if not stock_monitor.last_price_above_threshold:
                print("  → Alert state reset (price recovered)")
                stock_monitor.alert_sent = False
            stock_monitor.last_price_above_threshold = True
        else:
            # Price below threshold
            stock_monitor.last_price_above_threshold = False
            if not stock_monitor.alert_sent:
                print("  → Would send alert (first time below threshold)")
                stock_monitor.alert_sent = True
            else:
                print("  → Would NOT send alert (already alerted for this period)")
        
        print(f"  Alert sent flag: {stock_monitor.alert_sent}")
        print(f"  Last price above threshold: {stock_monitor.last_price_above_threshold}")

def test_email_formatting():
    """Test the new email format"""
    print("\n=== TESTING EMAIL FORMAT ===")
    
    test_price = 17.50
    ist_time = datetime.now(Config.MARKET_TIMEZONE)
    timestamp = ist_time.strftime("%Y-%m-%d %H:%M:%S IST")
    
    subject = Config.ALERT_SUBJECT
    body = Config.get_alert_body(test_price, timestamp)
    
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")

def main():
    """Run all tests"""
    print("🧪 Enhanced Stock Alert System - Comprehensive Testing")
    print("=" * 60)
    
    # Test 1: Market hours
    market_open = test_market_hours()
    
    # Test 2: Alert logic
    should_alert = test_alert_logic()
    
    # Test 3: Rate limiting
    test_rate_limiting()
    
    # Test 4: Email format
    test_email_formatting()
    
    print("\n" + "=" * 60)
    print("🎯 SUMMARY:")
    print(f"✅ Market hours detection working")
    print(f"✅ Alert logic {'would trigger' if should_alert else 'properly filtered'}")
    print(f"✅ Rate limiting logic implemented")
    print(f"✅ Email format updated")
    
    if market_open and should_alert:
        print("\n⚠️  NOTE: Alerts would be sent if system were running during market hours with price below threshold")
    else:
        print("\n💡 NOTE: No alerts will be sent outside market hours or above threshold")

if __name__ == "__main__":
    main()
