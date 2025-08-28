# � YesBank-StockAlert-Dashboard

**Professional Real-Time Stock Monitoring System for Yes Bank (YESBANK.NS)**

A comprehensive Python-based stock alert system featuring both CLI and GUI interfaces with live charts, intelligent alerting, and email notifications for Yes Bank stock monitoring.

---

## 🌟 Project Overview

**YesBank-StockAlert-Dashboard** is a sophisticated stock monitoring solution that provides real-time tracking of Yes Bank (YESBANK.NS) stock prices with advanced alerting capabilities. The system features both command-line and graphical user interfaces, making it suitable for both automated monitoring and interactive analysis.

### 🎯 **Key Features**

- **📊 Real-Time Monitoring**: Live stock price tracking with 1-minute intervals during market hours
- **🚨 Smart Alerts**: Intelligent threshold-based email notifications with spam prevention
- **📈 Interactive GUI**: Professional dashboard with live charts and volume analysis
- **⏰ Market Hours Aware**: NSE trading hours detection (9:15 AM - 3:30 PM IST)
- **📧 Email Integration**: Gmail SMTP notifications with retry logic
- **🔄 Dual Interface**: Both CLI and GUI modes for different use cases
- **🛡️ Error Handling**: Robust error handling with automatic recovery
- **☁️ Cloud Ready**: Deployment-ready for Render, Heroku, or local servers

---

## 🚀 Quick Start

### **Option 1: GUI Dashboard (Recommended)**
```bash
# Clone the repository
git clone https://github.com/yourusername/YesBank-StockAlert-Dashboard.git
cd YesBank-StockAlert-Dashboard

# Run the GUI dashboard
.\run_dashboard.bat
```

### **Option 2: CLI Mode**
```bash
# Activate environment and run CLI version
.\stock_alert_env\Scripts\Activate.ps1
python main.py
```

### **Option 3: Auto-Setup**
```bash
# Automatic dependency installation and launch
python launcher.py
```

### Local Development Setup

1. **Clone/Download the project**
   ```bash
   cd "c:\Users\baves\Downloads\Yes Bank Project"
   ```

2. **Create Python virtual environment**
   ```bash
   python -m venv stock_alert_env
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   stock_alert_env\Scripts\activate
   
   # Linux/Mac
   source stock_alert_env/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   # Copy the template
   copy .env.example .env
   
   # Edit .env file with your credentials (already configured)
   ```

6. **Test the system**
   ```bash
   python main.py --test
   ```

7. **Run the monitoring system**
   ```bash
   python main.py
   ```

## 📧 Email Configuration

The system is pre-configured with your Gmail credentials:
- **Email**: baveshchowdary1@gmail.com
- **App Password**: ilsp zgmj pfhj iyli

### Gmail App Password Setup (Already Done)
Your app password is already configured. If you need to generate a new one:
1. Go to Google Account Settings
2. Enable 2-Factor Authentication
3. Generate App Password for "Mail"
4. Use the 16-character password in the configuration

## 📊 Stock Monitoring Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| Stock Symbol | YESBANK.NS | Yes Bank NSE listing |
| Price Threshold | ₹17.99 | Alert trigger point |
| Check Interval | 60 seconds | Price check frequency |
| Alert Cooldown | 30 minutes | Minimum time between alerts |

## 🔄 System Workflow

1. **Price Fetching**: System fetches current Yes Bank price from Yahoo Finance
2. **Threshold Check**: Compares price against ₹17.99 threshold
3. **Alert Logic**: If price < ₹17.99 AND cooldown period has passed:
   - Sends email alert
   - Starts 30-minute cooldown timer
4. **Reset Logic**: When price goes back above ₹17.99, alert state resets
5. **Continuous Loop**: Repeats every 60 seconds

## 📈 Testing Instructions

### Test System Components
```bash
# Test all components
python main.py --test

# Manual price check
python -c "from stock_monitor import StockMonitor; from email_service import EmailService; sm = StockMonitor(EmailService()); print(f'Current price: ₹{sm.get_current_price():.2f}')"

# Test email service
python -c "from email_service import EmailService; es = EmailService(); print('Email test:', es.test_connection())"
```

### Verify Alert Logic
1. **Normal Operation**: Run system when price is above ₹17.99
2. **Alert Testing**: Wait for natural price drop or temporarily modify threshold in config.py
3. **Cooldown Testing**: Verify no duplicate alerts sent within 30 minutes
4. **Recovery Testing**: Verify alert state resets when price recovers

## ☁️ Render Deployment Guide

### Prerequisites
- GitHub account
- Render account (free tier available)
- This project pushed to GitHub repository

### Step-by-Step Deployment

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Stock Alert System"
   git remote add origin https://github.com/yourusername/yes-bank-stock-alert.git
   git push -u origin main
   ```

2. **Create Render Service**
   - Go to [Render Dashboard](https://render.com)
   - Click "New" → "Background Worker"
   - Connect your GitHub repository
   - Select the project repository

3. **Configure Service Settings**
   ```
   Name: yes-bank-stock-alert
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   ```

4. **Set Environment Variables**
   In Render dashboard, add these environment variables:
   ```
   EMAIL_ADDRESS = baveshchowdary1@gmail.com
   EMAIL_PASSWORD = ilsp zgmj pfhj iyli
   ```

5. **Deploy**
   - Click "Create Background Worker"
   - Wait for deployment to complete
   - Monitor logs for successful startup

### Render Configuration Files

**Procfile** (already created):
```
worker: python main.py
```

**requirements.txt** (already created):
```
yfinance==0.2.28
schedule==1.2.1
python-dotenv==1.0.0
requests==2.31.0
pytz==2023.3
```

## 📊 Monitoring & Logs

### Local Monitoring
```bash
# View real-time logs
tail -f stock_alert.log

# Monitor system status
python main.py --test
```

### Render Monitoring
1. Go to Render dashboard
2. Click on your service
3. View "Logs" tab for real-time monitoring
4. Check "Events" tab for deployment history

### Log Analysis
The system logs include:
- Price checks with timestamps
- Alert triggers and cooldown status
- Error messages with retry attempts
- System health statistics

## 🛠️ Customization Guide

### Modify Price Threshold
Edit `config.py`:
```python
PRICE_THRESHOLD = 18.50  # New threshold
```

### Change Check Interval
Edit `config.py`:
```python
CHECK_INTERVAL = 120  # Check every 2 minutes
```

### Modify Alert Cooldown
Edit `config.py`:
```python
ALERT_COOLDOWN = 3600  # 1 hour cooldown
```

### Add Multiple Stocks
1. Create new configuration for each stock
2. Modify `StockMonitor` to accept symbol parameter
3. Run multiple instances or implement multi-stock logic

## 🚨 Troubleshooting

### Common Issues

**1. Email Authentication Failed**
```
Solution: Verify app password is correct and 2FA is enabled
Test: python -c "from email_service import EmailService; EmailService().test_connection()"
```

**2. Stock Price Not Fetching**
```
Solution: Check internet connection and Yahoo Finance availability
Test: python -c "import yfinance as yf; print(yf.Ticker('YESBANK.NS').history(period='1d'))"
```

**3. No Alerts Received**
```
Possible Causes:
- Price is above threshold
- Cooldown period is active
- Email delivery issues
Check logs for detailed error messages
```

**4. Render Deployment Issues**
```
Common Solutions:
- Ensure all environment variables are set
- Check build logs for dependency issues
- Verify Procfile format is correct
```

### Debug Commands
```bash
# Check current price
python -c "from stock_monitor import StockMonitor; from email_service import EmailService; print(StockMonitor(EmailService()).get_current_price())"

# Test email
python -c "from email_service import EmailService; EmailService().send_alert(17.50)"

# Check logs
cat stock_alert.log | tail -50
```

## 💰 Cost Optimization

### Render Free Tier
- 750 hours/month free (more than enough for 24/7 operation)
- No credit card required initially
- Perfect for this lightweight application

### Resource Usage
- **CPU**: Minimal (price checks every minute)
- **Memory**: < 100MB typical usage
- **Network**: Minimal (Yahoo Finance API calls)

## 🔮 Future Enhancements

### Multi-Stock Support
```python
# Example configuration for multiple stocks
STOCKS_CONFIG = {
    'YESBANK.NS': {'threshold': 17.99, 'email': 'alerts@example.com'},
    'RELIANCE.NS': {'threshold': 2500.00, 'email': 'alerts@example.com'}
}
```

### Advanced Alerts
- SMS notifications via Twilio
- Slack/Discord webhooks
- Technical analysis indicators
- Percentage-based thresholds

### Enhanced Monitoring
- Web dashboard for status monitoring
- Historical price analysis
- Alert frequency analytics
- Performance metrics

## 📞 Support

### System Status
Check if the system is running correctly:
```bash
python main.py --test
```

### Contact Information
- Monitor logs regularly for any issues
- System is designed to be self-healing with retry logic
- Most issues are temporary network problems that resolve automatically

## 📝 File Structure

```
Yes Bank Project/
├── main.py              # Main application entry point
├── config.py            # Configuration management
├── email_service.py     # Email notification handling
├── stock_monitor.py     # Stock price monitoring logic
├── requirements.txt     # Python dependencies
├── Procfile            # Render deployment configuration
├── .env.example        # Environment variables template
├── README.md           # This documentation
└── stock_alert.log     # Application logs (generated)
```

## ✅ Success Checklist

- [ ] Python 3.11 virtual environment created
- [ ] All dependencies installed via requirements.txt
- [ ] Email credentials configured and tested
- [ ] Stock price fetching working
- [ ] Alert logic tested with appropriate threshold
- [ ] System running locally without errors
- [ ] GitHub repository created and code pushed
- [ ] Render service created and deployed
- [ ] Environment variables set in Render
- [ ] 24/7 monitoring confirmed in Render logs
- [ ] Email alerts received when price drops below threshold
- [ ] Cooldown mechanism prevents spam alerts
- [ ] System recovers gracefully from errors

---

**🎉 Your Stock Alert Automation System is now ready for 24/7 operation!**

The system will continuously monitor Yes Bank stock price and send you email alerts whenever the price drops below ₹17.99, with intelligent cooldown to prevent spam. Monitor the Render logs to ensure everything is working smoothly.
