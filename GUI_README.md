# 📈 Yes Bank Stock Alert Dashboard

A comprehensive GUI-based stock monitoring system for Yes Bank (YESBANK.NS) with live charts, real-time alerts, and email notifications.

## 🌟 Features

### 📊 **Live Data Monitoring**
- Real-time stock price tracking
- Live price charts with candlestick visualization
- Trading volume analysis with color-coded bars
- Market hours detection (NSE: 9:15 AM - 3:30 PM IST)

### 🚨 **Smart Alerting System**
- Customizable price threshold alerts
- Email notifications when price crosses threshold
- State-based alerting (prevents spam emails)
- Market hours filtering (alerts only during trading hours)

### 💻 **Interactive GUI Dashboard**
- Dark theme modern interface
- Real-time updating charts
- Price change indicators with colors
- Market status display
- Data point counter and refresh rate

### 📧 **Email Integration**
- Gmail SMTP integration
- Test email functionality
- Professional alert formatting
- Retry logic for reliability

## 🚀 Quick Start

### Option 1: Using the Batch Script (Recommended)
```bash
# Double-click or run in terminal:
run_dashboard.bat
```

### Option 2: Manual Activation
```bash
# Activate virtual environment
.\stock_alert_env\Scripts\Activate.ps1

# Install dependencies (if needed)
pip install -r gui_requirements.txt

# Run dashboard
python stock_dashboard_gui.py
```

### Option 3: Using Launcher
```bash
# Auto-installs dependencies and runs
python launcher.py
```

## 📋 GUI Dashboard Components

### 🎯 **Header Section**
- **Stock Title**: YES BANK (YESBANK.NS) Live Dashboard
- **Current Time**: Real-time clock
- **Price Display**: Current stock price in ₹
- **Change Indicator**: Price change with ▲/▼ symbols and colors
- **Volume**: Trading volume (formatted: 1.2M for millions)
- **Market Status**: 🟢 OPEN / 🔴 CLOSED

### 📈 **Charts Section**
- **Price Chart**: Live line chart with threshold line
- **Volume Chart**: Color-coded bars (green=up, red=down)
- **Zoom & Pan**: Interactive matplotlib integration
- **Auto-scaling**: Automatic axis adjustment

### ⚙️ **Control Panel**

#### **Alert Settings**
- **Threshold Price**: Editable price threshold (₹)
- **Update Button**: Apply new threshold
- **Status Display**: Current alert status

#### **Action Buttons**
- **📧 Test Email**: Send test notification
- **🔄 Refresh Data**: Force data refresh
- **🗑️ Clear Chart**: Clear all chart data

#### **Data Information**
- **Data Points**: Number of stored price points
- **Last Update**: Time of most recent data fetch
- **Refresh Rate**: Current update frequency

### 📊 **Status Bar**
- **System Status**: Current operation status
- **Connection Status**: Yahoo Finance connection health

## ⚡ Real-Time Features

### 🕐 **Update Frequencies**
- **Market Open**: Updates every 5 seconds
- **Market Closed**: Updates every 30 seconds
- **GUI Refresh**: Every 1 second
- **Chart Redraw**: After each data update

### 🎯 **Smart Alerting Logic**
```python
# Alert is sent when:
1. Price crosses ABOVE threshold
2. Previous price was BELOW threshold
3. Market is currently OPEN
4. No alert sent for this crossing

# Alert is reset when:
1. Price goes BELOW threshold
2. Ready for next crossing alert
```

### 📱 **Market Hours Detection**
```python
# NSE Trading Hours (IST):
Market Open:  09:15 AM
Market Close: 03:30 PM
Trading Days: Monday to Friday
Holidays: Automatically detected
```

## 🔧 Configuration

### 📧 **Email Settings** (.env file)
```env
EMAIL_ADDRESS=baveshchowdary1@gmail.com
EMAIL_PASSWORD=ilsp zgmj pfhj iyli
```

### 📊 **Stock Settings** (config.py)
```python
STOCK_SYMBOL = "YESBANK.NS"
PRICE_THRESHOLD = 18.00
CHECK_INTERVAL = 60
```

## 🎨 GUI Themes & Styling

### 🌙 **Dark Theme**
- Background: `#1e1e1e` (Dark gray)
- Charts: `#2e2e2e` (Lighter gray)
- Text: White/Cyan
- Alerts: Red highlights

### 📊 **Chart Colors**
- **Price Line**: Cyan
- **Threshold Line**: Red dashed
- **Volume Bars**: Green (up) / Red (down)
- **Grid**: White with 30% transparency

## 🔍 Live Dashboard Screenshots

### 📈 **Main Dashboard View**
```
┌─────────────────────────────────────────────────────────────┐
│ 📈 YES BANK (YESBANK.NS) Live Dashboard    2025-08-28 23:37 │
├─────────────────────────────────────────────────────────────┤
│ Price: ₹18.45  ▲ ₹0.25 (+1.38%)  Volume: 2.3M  Market: 🔴  │
├─────────────────────────────────────────────────────────────┤
│                    📊 LIVE PRICE CHART                      │
│ ₹19.00 ┤                                          ┌─────     │
│ ₹18.50 ┤                    ╭─────╮              │            │
│ ₹18.00 ┤────────────────────┴─────┴──────────────┴─────     │ <- Threshold
│ ₹17.50 ┤                                                     │
│        └─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────      │
│            9:15  10:00 11:00 12:00 13:00 14:00 15:00       │
│                    📊 TRADING VOLUME                        │
│   2M   ┤     ▌                      ▌▌                      │
│   1M   ┤   ▌ ▌ ▌   ▌           ▌   ▌▌▌  ▌                  │
│   0    └─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────      │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Troubleshooting

### ❌ **Common Issues**

#### **"ModuleNotFoundError"**
```bash
# Solution: Activate virtual environment
.\stock_alert_env\Scripts\Activate.ps1
pip install -r gui_requirements.txt
```

#### **"No price data found"**
```bash
# Normal when market is closed
# Dashboard will show: "Market: 🔴 CLOSED"
# Data will resume when market opens
```

#### **Email not sending**
```bash
# Check .env file settings
# Test with: 📧 Test Email button
# Verify Gmail app password
```

### 🔧 **Performance Tips**

#### **Reduce Memory Usage**
- Dashboard keeps only last 100 data points
- Auto-clears old data to prevent memory buildup

#### **Improve Responsiveness**
- Uses background threading for data fetching
- Non-blocking GUI updates
- Separate threads for network calls

## 📊 Data Sources & APIs

### 📈 **Yahoo Finance Integration**
```python
# Real-time data fetching:
yfinance.Ticker("YESBANK.NS")
  .history(period="1d", interval="1m")

# Data includes:
- Current Price (₹)
- Trading Volume
- Price Change (₹ and %)
- Historical Data (1-minute intervals)
```

### 🌐 **Market Data Quality**
- **Delay**: ~15 minutes (standard for retail)
- **Accuracy**: High during market hours
- **Availability**: 24/7 (historical), Live during trading

## 🎯 Usage Examples

### 📧 **Setting Up Alerts**
1. Open dashboard: `run_dashboard.bat`
2. Set threshold: Enter price in "Threshold Price" field
3. Click "Update Threshold"
4. Test email: Click "📧 Test Email"

### 📊 **Monitoring During Trading**
1. Dashboard auto-updates every 5 seconds during market hours
2. Watch live price chart for trends
3. Volume bars show trading activity
4. Alerts sent automatically when threshold crossed

### 🔍 **Analyzing After Hours**
1. Dashboard shows last trading day data
2. Charts remain interactive for analysis
3. Market status shows "🔴 CLOSED"
4. Next update when market reopens

## 🚀 Advanced Features

### 📊 **Chart Interactions**
- **Zoom**: Mouse wheel on chart area
- **Pan**: Click and drag on chart
- **Reset**: Use "🗑️ Clear Chart" button

### ⚡ **Real-time Updates**
- Price updates every 5 seconds (market hours)
- Chart redraws automatically
- Status updates in real-time
- Email alerts sent instantly

### 🎯 **Smart State Management**
- Remembers alert state across price movements
- Prevents duplicate alerts for same threshold crossing
- Auto-resets when price moves away from threshold

## 📞 Support & Contact

Created for comprehensive Yes Bank stock monitoring with professional-grade alerting and visualization.

**System Requirements:**
- Python 3.11+
- Windows 10/11
- Internet connection
- Gmail account (for alerts)

**Dependencies:**
- yfinance, matplotlib, tkinter, pandas, numpy, pytz, schedule, python-dotenv

---

**🎉 Happy Trading! Monitor Yes Bank stock prices with confidence using this professional dashboard!** 📈
