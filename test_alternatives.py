import yfinance as yf

# Test alternative stocks that are definitely active
test_symbols = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS']

for symbol in test_symbols:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        if not data.empty:
            print(f'{symbol}: Rs.{data["Close"].iloc[-1]:.2f} - WORKING')
            break
        else:
            print(f'{symbol}: No data')
    except Exception as e:
        print(f'{symbol}: Error - {e}')
