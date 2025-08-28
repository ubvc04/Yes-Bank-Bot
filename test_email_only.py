#!/usr/bin/env python3
"""
Quick test for email functionality only
"""

import os
import sys
import logging
from datetime import datetime
from email_service import EmailService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_email_functionality():
    print("=== TESTING EMAIL FUNCTIONALITY ONLY ===")
    
    # Create email service instance
    email_service = EmailService()
    
    # Test email with sample data
    test_price = 18.50
    test_threshold = 18.00
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    subject = f"🚨 YES BANK Stock Alert - Price Above ₹{test_threshold}"
    message = f"""
YES BANK (YESBANK.NS) Stock Alert

💰 Current Price: ₹{test_price:.2f}
🎯 Alert Threshold: ₹{test_threshold:.2f}
📈 Status: ABOVE THRESHOLD
⏰ Time: {current_time}

This is a test email to verify the alert system is working correctly.

---
Stock Alert Automation System
"""
    
    print(f"Sending test email...")
    print(f"Subject: {subject}")
    print(f"Current time: {current_time}")
    
    try:
        email_service.send_alert(subject, message)
        print("✅ Email sent successfully!")
        print("\nCheck your inbox for the test alert email.")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    success = test_email_functionality()
    if success:
        print("\n🎉 Email service is working correctly!")
        print("You can now run the main stock alert system:")
        print("python main.py")
    else:
        print("\n❌ Email service needs to be configured properly.")
        print("Please check your .env file and email settings.")
