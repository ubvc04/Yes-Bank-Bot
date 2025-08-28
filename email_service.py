"""
Email service for sending stock alert notifications
Handles SMTP connection, email composition, and delivery
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
from config import Config

class EmailService:
    """Handles email notifications for stock alerts"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.email_address = Config.EMAIL_ADDRESS
        self.email_password = Config.EMAIL_PASSWORD
        
    def send_alert(self, current_price, timestamp=None):
        """
        Send stock price alert email
        
        Args:
            current_price (float): Current stock price
            timestamp (str, optional): Alert timestamp
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
        
        try:
            # Create email message
            message = self._create_email_message(current_price, timestamp)
            
            # Send email with retry logic
            return self._send_with_retry(message)
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {str(e)}")
            return False
    
    def _create_email_message(self, current_price, timestamp):
        """Create formatted email message"""
        message = MIMEMultipart()
        message["From"] = self.email_address
        message["To"] = self.email_address
        message["Subject"] = Config.ALERT_SUBJECT
        
        # Create email body
        body = Config.get_alert_body(current_price, timestamp)
        message.attach(MIMEText(body, "plain"))
        
        return message
    
    def _send_with_retry(self, message):
        """Send email with retry logic"""
        for attempt in range(Config.MAX_RETRIES):
            try:
                # Create SMTP connection
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()  # Enable encryption
                server.login(self.email_address, self.email_password)
                
                # Send email
                text = message.as_string()
                server.sendmail(self.email_address, self.email_address, text)
                server.quit()
                
                self.logger.info(f"Email alert sent successfully on attempt {attempt + 1}")
                return True
                
            except smtplib.SMTPAuthenticationError as e:
                self.logger.error(f"SMTP Authentication failed: {str(e)}")
                return False  # Don't retry auth failures
                
            except smtplib.SMTPException as e:
                self.logger.warning(f"SMTP error on attempt {attempt + 1}: {str(e)}")
                if attempt < Config.MAX_RETRIES - 1:
                    self.logger.info(f"Retrying in {Config.RETRY_DELAY} seconds...")
                    time.sleep(Config.RETRY_DELAY)
                    
            except Exception as e:
                self.logger.warning(f"Unexpected error on attempt {attempt + 1}: {str(e)}")
                if attempt < Config.MAX_RETRIES - 1:
                    self.logger.info(f"Retrying in {Config.RETRY_DELAY} seconds...")
                    time.sleep(Config.RETRY_DELAY)
        
        self.logger.error(f"Failed to send email after {Config.MAX_RETRIES} attempts")
        return False
    
    def test_connection(self):
        """Test SMTP connection and authentication"""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.quit()
            self.logger.info("Email connection test successful")
            return True
        except Exception as e:
            self.logger.error(f"Email connection test failed: {str(e)}")
            return False
