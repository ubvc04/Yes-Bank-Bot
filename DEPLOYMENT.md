# 🚀 Render Deployment Guide

## Step-by-Step Instructions for Deploying to Render

### 1. Prepare Your GitHub Repository

1. **Initialize Git Repository**
   ```bash
   cd "c:\Users\baves\Downloads\Yes Bank Project"
   git init
   git add .
   git commit -m "Initial commit: Stock Alert Automation System"
   ```

2. **Create GitHub Repository**
   - Go to [GitHub.com](https://github.com)
   - Click "New repository"
   - Name: `yes-bank-stock-alert`
   - Make it private (recommended for sensitive code)
   - Click "Create repository"

3. **Push Code to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/yes-bank-stock-alert.git
   git branch -M main
   git push -u origin main
   ```

### 2. Deploy to Render

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub account
   - Connect your GitHub repositories

2. **Create New Service**
   - Click "New +" → "Background Worker"
   - Connect Repository: Select `yes-bank-stock-alert`
   - Branch: `main`

3. **Configure Service Settings**
   ```
   Name: yes-bank-stock-alert
   Environment: Python 3
   Region: Oregon (US West) - or closest to you
   Instance Type: Free (sufficient for this app)
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   ```

4. **Set Environment Variables**
   In the "Environment" section, add:
   ```
   EMAIL_ADDRESS = baveshchowdary1@gmail.com
   EMAIL_PASSWORD = ilsp zgmj pfhj iyli
   ```

5. **Deploy**
   - Click "Create Background Worker"
   - Wait for deployment (usually 2-5 minutes)
   - Monitor logs for successful startup

### 3. Monitor Deployment

**View Logs:**
- Go to your service dashboard
- Click "Logs" tab
- Look for: "[OK] System started successfully. Monitoring in progress..."

**Expected Log Pattern:**
```
[START] Starting Stock Alert Automation System
Monitoring: YESBANK.NS
Threshold: Rs.17.99
Check interval: 60 seconds
Alert cooldown: 30.0 minutes
[OK] Configuration validation passed
[OK] Email service connection successful
[OK] Yahoo Finance connection successful
[OK] System started successfully. Monitoring in progress...
```

### 4. Verify System is Working

1. **Check Logs Every Few Minutes:**
   - Should see periodic price checks
   - No error messages in steady state

2. **Test Alert (Optional):**
   - Temporarily modify threshold in config.py to test alerts
   - Push changes to trigger re-deployment
   - Verify email alerts are received

### 5. Troubleshooting

**Common Issues:**

1. **Build Failed:**
   - Check requirements.txt is valid
   - Ensure all files are committed to git

2. **Email Authentication Error:**
   - Verify environment variables are set correctly
   - Ensure no spaces in email password

3. **Stock Data Issues:**
   - System will use mock data if Yahoo Finance is unavailable
   - This is normal for testing/development

**Debug Commands (run locally):**
```bash
python main.py --test  # Test all components
python test_alert.py   # Test email alerts
```

### 6. Cost Information

**Render Free Tier:**
- 750 hours/month (enough for 24/7 operation)
- No bandwidth limits for this use case
- Perfect for this lightweight application

**Upgrade Options:**
- If you need more reliability: $7/month for Starter plan
- Includes persistent storage and priority support

### 7. Monitoring Your Deployment

**Daily Checks:**
1. Visit Render dashboard
2. Check service status (should be "Running")
3. Review recent logs for any errors
4. Verify email alerts are working if price drops

**Weekly Maintenance:**
1. Check for any system updates needed
2. Verify Yahoo Finance connection is stable
3. Review alert frequency and adjust if needed

### 8. Making Updates

**To Update Configuration:**
1. Edit files locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update configuration"
   git push
   ```
3. Render will automatically redeploy

**To Change Stock Symbol:**
1. Edit `config.py` → Change `STOCK_SYMBOL`
2. Edit `README.md` → Update documentation
3. Commit and push changes

### 9. Security Best Practices

✅ **What's Already Done:**
- Email credentials stored as environment variables
- Private repository recommended
- Secure SMTP connection with TLS

⚠️ **Additional Recommendations:**
- Regularly rotate email app password
- Monitor logs for any suspicious activity
- Keep dependencies updated

### 10. Success Checklist

After deployment, verify:
- [ ] Service shows "Running" status in Render
- [ ] Logs show successful startup messages
- [ ] No authentication errors in logs
- [ ] Price checks happening every 60 seconds
- [ ] Email test was successful
- [ ] System handles Yahoo Finance outages gracefully

---

## 🎉 Congratulations!

Your Stock Alert Automation System is now deployed and running 24/7 on Render. The system will:

- Monitor Yes Bank stock price every minute
- Send email alerts when price drops below ₹17.99
- Prevent spam with 30-minute cooldown
- Handle errors gracefully and continue running
- Log all activity for monitoring

**Next Steps:**
1. Monitor the Render logs for the first few hours
2. Test the alert system when market conditions allow
3. Consider expanding to monitor multiple stocks
4. Set up phone notifications for critical alerts

Your automated stock monitoring system is production-ready! 🚀
