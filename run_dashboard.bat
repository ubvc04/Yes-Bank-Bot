@echo off
echo 🚀 Starting Yes Bank Stock Dashboard...
echo.
echo 📊 Features:
echo   • Live stock price monitoring
echo   • Real-time charts and graphs
echo   • Price threshold alerts  
echo   • Email notifications
echo   • Market hours detection
echo.
echo 📈 Activating environment and launching dashboard...
echo.

cd /d "C:\Users\baves\Downloads\Yes Bank Project"
call stock_alert_env\Scripts\activate.bat
python stock_dashboard_gui.py

pause
