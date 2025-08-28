#!/usr/bin/env python3
"""
Yes Bank Stock Alert GUI Dashboard
Real-time stock monitoring with live charts and alerts
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import threading
import time
from config import Config
from email_service import EmailService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class YesBankDashboard:
    def __init__(self, root):
        self.root = root
        self.config = Config()
        self.email_service = EmailService()
        
        # Data storage
        self.price_data = []
        self.time_data = []
        self.volume_data = []
        
        # Alert state
        self.last_price_above_threshold = True
        self.alert_sent = False
        
        # Setup GUI
        self.setup_gui()
        
        # Start data fetching thread
        self.running = True
        self.data_thread = threading.Thread(target=self.data_fetcher, daemon=True)
        self.data_thread.start()
        
        # Setup auto-refresh
        self.root.after(1000, self.update_display)  # Update every second
        
    def setup_gui(self):
        """Setup the main GUI interface"""
        self.root.title("📈 Yes Bank Stock Alert Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#1e1e1e', foreground='#ffffff')
        style.configure('Info.TLabel', font=('Arial', 12), background='#1e1e1e', foreground='#ffffff')
        style.configure('Alert.TLabel', font=('Arial', 14, 'bold'), background='#1e1e1e', foreground='#ff4444')
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header section
        self.setup_header(main_frame)
        
        # Charts section
        self.setup_charts(main_frame)
        
        # Controls section
        self.setup_controls(main_frame)
        
        # Status section
        self.setup_status(main_frame)
        
    def setup_header(self, parent):
        """Setup header with stock info"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = ttk.Label(header_frame, text="📈 YES BANK (YESBANK.NS) Live Dashboard", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Current time
        self.time_label = ttk.Label(header_frame, text="", style='Info.TLabel')
        self.time_label.pack(side=tk.RIGHT)
        
        # Stock info frame
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Price display
        self.price_label = ttk.Label(info_frame, text="Price: Loading...", style='Title.TLabel')
        self.price_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Change display
        self.change_label = ttk.Label(info_frame, text="Change: --", style='Info.TLabel')
        self.change_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Volume display
        self.volume_label = ttk.Label(info_frame, text="Volume: --", style='Info.TLabel')
        self.volume_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Market status
        self.market_status_label = ttk.Label(info_frame, text="Market: --", style='Info.TLabel')
        self.market_status_label.pack(side=tk.RIGHT)
        
    def setup_charts(self, parent):
        """Setup matplotlib charts"""
        chart_frame = ttk.Frame(parent)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create figure with subplots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8), facecolor='#1e1e1e')
        self.fig.patch.set_facecolor('#1e1e1e')
        
        # Price chart
        self.ax1.set_facecolor('#2e2e2e')
        self.ax1.set_title('Yes Bank Stock Price (Live)', color='white', fontsize=14, fontweight='bold')
        self.ax1.set_ylabel('Price (₹)', color='white')
        self.ax1.tick_params(colors='white')
        self.ax1.grid(True, alpha=0.3)
        
        # Volume chart
        self.ax2.set_facecolor('#2e2e2e')
        self.ax2.set_title('Trading Volume', color='white', fontsize=12)
        self.ax2.set_ylabel('Volume', color='white')
        self.ax2.set_xlabel('Time', color='white')
        self.ax2.tick_params(colors='white')
        self.ax2.grid(True, alpha=0.3)
        
        # Embed charts in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        plt.tight_layout()
        
    def setup_controls(self, parent):
        """Setup control buttons and settings"""
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Alert settings
        alert_frame = ttk.LabelFrame(controls_frame, text="Alert Settings")
        alert_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ttk.Label(alert_frame, text="Threshold Price (₹):").pack(anchor=tk.W)
        self.threshold_var = tk.StringVar(value=str(self.config.PRICE_THRESHOLD))
        threshold_entry = ttk.Entry(alert_frame, textvariable=self.threshold_var, width=10)
        threshold_entry.pack(anchor=tk.W, pady=(0, 5))
        
        update_btn = ttk.Button(alert_frame, text="Update Threshold", command=self.update_threshold)
        update_btn.pack(anchor=tk.W, pady=(0, 5))
        
        # Alert status
        self.alert_status_label = ttk.Label(alert_frame, text="Status: Ready", style='Info.TLabel')
        self.alert_status_label.pack(anchor=tk.W)
        
        # Action buttons
        actions_frame = ttk.LabelFrame(controls_frame, text="Actions")
        actions_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        test_email_btn = ttk.Button(actions_frame, text="📧 Test Email", command=self.test_email)
        test_email_btn.pack(pady=2, fill=tk.X)
        
        refresh_btn = ttk.Button(actions_frame, text="🔄 Refresh Data", command=self.force_refresh)
        refresh_btn.pack(pady=2, fill=tk.X)
        
        clear_btn = ttk.Button(actions_frame, text="🗑️ Clear Chart", command=self.clear_chart)
        clear_btn.pack(pady=2, fill=tk.X)
        
        # Data info
        info_frame = ttk.LabelFrame(controls_frame, text="Data Info")
        info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.data_points_label = ttk.Label(info_frame, text="Data Points: 0")
        self.data_points_label.pack(anchor=tk.W)
        
        self.last_update_label = ttk.Label(info_frame, text="Last Update: --")
        self.last_update_label.pack(anchor=tk.W)
        
        self.refresh_rate_label = ttk.Label(info_frame, text="Refresh: 30s")
        self.refresh_rate_label.pack(anchor=tk.W)
        
    def setup_status(self, parent):
        """Setup status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(status_frame, text="🟢 System Ready - Monitoring Yes Bank stock...", style='Info.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        # Connection status
        self.connection_label = ttk.Label(status_frame, text="📡 Yahoo Finance: Connected", style='Info.TLabel')
        self.connection_label.pack(side=tk.RIGHT)
        
    def is_market_open(self):
        """Check if NSE market is open"""
        try:
            ist = pytz.timezone('Asia/Kolkata')
            now = datetime.now(ist)
            current_time = now.time()
            
            # Market hours: 9:15 AM to 3:30 PM IST, Monday to Friday
            market_open = now.replace(hour=9, minute=15, second=0, microsecond=0).time()
            market_close = now.replace(hour=15, minute=30, second=0, microsecond=0).time()
            
            is_weekday = now.weekday() < 5  # Monday = 0, Sunday = 6
            is_trading_hours = market_open <= current_time <= market_close
            
            return is_weekday and is_trading_hours
        except Exception:
            return False
            
    def get_stock_data(self):
        """Fetch current stock data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(self.config.STOCK_SYMBOL)
            
            # Get current price
            hist = ticker.history(period="1d", interval="1m")
            if hist.empty:
                return None
                
            current_price = float(hist['Close'].iloc[-1])
            current_volume = int(hist['Volume'].iloc[-1])
            
            # Calculate change
            if len(hist) > 1:
                prev_price = float(hist['Close'].iloc[-2])
                price_change = current_price - prev_price
                change_percent = (price_change / prev_price) * 100
            else:
                price_change = 0
                change_percent = 0
                
            return {
                'price': current_price,
                'volume': current_volume,
                'change': price_change,
                'change_percent': change_percent,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logging.error(f"Error fetching stock data: {e}")
            return None
            
    def check_price_alert(self, current_price):
        """Check if price alert should be sent"""
        try:
            threshold = float(self.threshold_var.get())
            
            # Check if price crossed threshold
            price_above_threshold = current_price >= threshold
            
            # Send alert if price crossed above threshold and we haven't sent one yet
            if price_above_threshold and not self.last_price_above_threshold and not self.alert_sent:
                self.send_price_alert(current_price, threshold)
                self.alert_sent = True
                
            # Reset alert flag if price goes below threshold
            if not price_above_threshold:
                self.alert_sent = False
                
            self.last_price_above_threshold = price_above_threshold
            
        except Exception as e:
            logging.error(f"Error checking price alert: {e}")
            
    def send_price_alert(self, current_price, threshold):
        """Send email alert for price threshold"""
        try:
            subject = f"🚨 YES BANK Alert - Price Above ₹{threshold}"
            message = f"""
YES BANK (YESBANK.NS) Stock Alert

💰 Current Price: ₹{current_price:.2f}
🎯 Alert Threshold: ₹{threshold:.2f}
📈 Status: ABOVE THRESHOLD
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

The stock price has crossed your alert threshold!

---
Stock Alert Dashboard
"""
            
            self.email_service.send_alert(subject, message)
            self.status_label.config(text=f"🔔 Alert sent! Price: ₹{current_price:.2f}")
            
        except Exception as e:
            logging.error(f"Error sending alert: {e}")
            self.status_label.config(text=f"❌ Alert failed: {str(e)}")
            
    def data_fetcher(self):
        """Background thread to fetch stock data"""
        while self.running:
            try:
                data = self.get_stock_data()
                if data:
                    # Store data
                    self.price_data.append(data['price'])
                    self.time_data.append(data['timestamp'])
                    self.volume_data.append(data['volume'])
                    
                    # Keep only last 100 data points
                    if len(self.price_data) > 100:
                        self.price_data.pop(0)
                        self.time_data.pop(0)
                        self.volume_data.pop(0)
                        
                    # Check for alerts (only during market hours)
                    if self.is_market_open():
                        self.check_price_alert(data['price'])
                        
                # Sleep for 30 seconds (or 5 seconds during market hours)
                sleep_time = 5 if self.is_market_open() else 30
                time.sleep(sleep_time)
                
            except Exception as e:
                logging.error(f"Data fetcher error: {e}")
                time.sleep(30)
                
    def update_display(self):
        """Update the GUI display"""
        try:
            # Update time
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.time_label.config(text=current_time)
            
            # Update market status
            market_open = self.is_market_open()
            market_text = "🟢 OPEN" if market_open else "🔴 CLOSED"
            self.market_status_label.config(text=f"Market: {market_text}")
            
            # Update data info
            self.data_points_label.config(text=f"Data Points: {len(self.price_data)}")
            if self.time_data:
                last_update = self.time_data[-1].strftime('%H:%M:%S')
                self.last_update_label.config(text=f"Last Update: {last_update}")
                
            # Update price display
            if self.price_data:
                current_price = self.price_data[-1]
                self.price_label.config(text=f"Price: ₹{current_price:.2f}")
                
                # Update change
                if len(self.price_data) > 1:
                    prev_price = self.price_data[-2]
                    change = current_price - prev_price
                    change_percent = (change / prev_price) * 100
                    
                    change_color = "green" if change >= 0 else "red"
                    change_symbol = "▲" if change >= 0 else "▼"
                    
                    change_text = f"{change_symbol} ₹{abs(change):.2f} ({change_percent:+.2f}%)"
                    self.change_label.config(text=f"Change: {change_text}")
                    
                # Update volume
                if self.volume_data:
                    volume = self.volume_data[-1]
                    volume_text = f"{volume:,}" if volume < 1000000 else f"{volume/1000000:.1f}M"
                    self.volume_label.config(text=f"Volume: {volume_text}")
                    
            # Update charts
            self.update_charts()
            
            # Update alert status
            threshold = float(self.threshold_var.get())
            if self.price_data and self.price_data[-1] >= threshold:
                self.alert_status_label.config(text="Status: 🔔 Above Threshold")
            else:
                self.alert_status_label.config(text="Status: 📊 Monitoring")
                
        except Exception as e:
            logging.error(f"Display update error: {e}")
            
        # Schedule next update
        self.root.after(1000, self.update_display)
        
    def update_charts(self):
        """Update the matplotlib charts"""
        try:
            if not self.price_data or not self.time_data:
                return
                
            # Clear previous plots
            self.ax1.clear()
            self.ax2.clear()
            
            # Plot price data
            self.ax1.plot(self.time_data, self.price_data, 'cyan', linewidth=2, label='Price')
            
            # Add threshold line
            threshold = float(self.threshold_var.get())
            self.ax1.axhline(y=threshold, color='red', linestyle='--', alpha=0.7, label=f'Threshold ₹{threshold}')
            
            # Customize price chart
            self.ax1.set_facecolor('#2e2e2e')
            self.ax1.set_title('Yes Bank Stock Price (Live)', color='white', fontsize=14, fontweight='bold')
            self.ax1.set_ylabel('Price (₹)', color='white')
            self.ax1.tick_params(colors='white')
            self.ax1.grid(True, alpha=0.3)
            self.ax1.legend()
            
            # Plot volume data
            if self.volume_data:
                colors = ['green' if i == 0 or self.price_data[i] >= self.price_data[i-1] else 'red' 
                         for i in range(len(self.volume_data))]
                self.ax2.bar(self.time_data, self.volume_data, color=colors, alpha=0.7, width=0.0008)
                
            # Customize volume chart
            self.ax2.set_facecolor('#2e2e2e')
            self.ax2.set_title('Trading Volume', color='white', fontsize=12)
            self.ax2.set_ylabel('Volume', color='white')
            self.ax2.set_xlabel('Time', color='white')
            self.ax2.tick_params(colors='white')
            self.ax2.grid(True, alpha=0.3)
            
            # Format x-axis
            if len(self.time_data) > 0:
                self.ax1.tick_params(axis='x', rotation=45)
                self.ax2.tick_params(axis='x', rotation=45)
                
            plt.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            logging.error(f"Chart update error: {e}")
            
    def update_threshold(self):
        """Update the alert threshold"""
        try:
            new_threshold = float(self.threshold_var.get())
            self.config.PRICE_THRESHOLD = new_threshold
            self.status_label.config(text=f"📊 Threshold updated to ₹{new_threshold}")
            messagebox.showinfo("Success", f"Alert threshold updated to ₹{new_threshold}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for threshold")
            
    def test_email(self):
        """Test email functionality"""
        try:
            current_price = self.price_data[-1] if self.price_data else 18.50
            threshold = float(self.threshold_var.get())
            
            subject = f"🧪 Test Alert - YES BANK Stock Monitor"
            message = f"""
This is a test email from YES BANK Stock Dashboard

💰 Current Price: ₹{current_price:.2f}
🎯 Alert Threshold: ₹{threshold:.2f}
⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

If you received this email, the alert system is working correctly!

---
Stock Alert Dashboard
"""
            
            self.email_service.send_alert(subject, message)
            self.status_label.config(text="📧 Test email sent successfully!")
            messagebox.showinfo("Success", "Test email sent successfully!\nCheck your inbox.")
            
        except Exception as e:
            error_msg = f"Failed to send test email: {str(e)}"
            self.status_label.config(text=f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)
            
    def force_refresh(self):
        """Force refresh of stock data"""
        self.status_label.config(text="🔄 Refreshing data...")
        
    def clear_chart(self):
        """Clear all chart data"""
        self.price_data.clear()
        self.time_data.clear()
        self.volume_data.clear()
        self.ax1.clear()
        self.ax2.clear()
        self.canvas.draw()
        self.status_label.config(text="🗑️ Chart data cleared")
        
    def on_closing(self):
        """Handle application closing"""
        self.running = False
        if hasattr(self, 'data_thread'):
            self.data_thread.join(timeout=1)
        self.root.destroy()

def main():
    """Main function to run the dashboard"""
    root = tk.Tk()
    
    # Set dark theme
    root.tk_setPalette(background='#1e1e1e', foreground='white')
    
    # Create dashboard
    dashboard = YesBankDashboard(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", dashboard.on_closing)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (1200 // 2)
    y = (root.winfo_screenheight() // 2) - (800 // 2)
    root.geometry(f"1200x800+{x}+{y}")
    
    print("🚀 Starting Yes Bank Stock Dashboard...")
    print("📊 Features:")
    print("   • Live stock price monitoring")
    print("   • Real-time charts and graphs") 
    print("   • Price threshold alerts")
    print("   • Email notifications")
    print("   • Market hours detection")
    print("\n📈 Dashboard will open in a new window...")
    
    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
