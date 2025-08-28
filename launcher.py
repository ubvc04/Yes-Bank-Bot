#!/usr/bin/env python3
"""
Simple launcher for the Yes Bank Stock Dashboard
This will install dependencies if needed and launch the GUI
"""

import sys
import subprocess
import os

def check_and_install_packages():
    """Check if required packages are installed"""
    required_packages = [
        'matplotlib',
        'yfinance',
        'pandas',
        'numpy',
        'pytz',
        'schedule',
        'python-dotenv',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Installing missing packages: {', '.join(missing_packages)}")
        for package in missing_packages:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    
    return len(missing_packages) == 0

def main():
    print("🚀 Yes Bank Stock Dashboard Launcher")
    print("=" * 50)
    
    # Check and install packages
    print("📦 Checking dependencies...")
    if check_and_install_packages():
        print("✅ All dependencies ready!")
    else:
        print("❌ Failed to install dependencies")
        return
    
    # Import and run dashboard
    try:
        print("📈 Launching dashboard...")
        from stock_dashboard_gui import main as run_dashboard
        run_dashboard()
    except ImportError as e:
        print(f"❌ Failed to import dashboard: {e}")
        print("Make sure stock_dashboard_gui.py is in the same directory")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")

if __name__ == "__main__":
    main()
