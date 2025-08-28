import yfinance as yf

# Test Yes Bank symbol
ticker = yf.Ticker('YESBANK.NS')
print('Testing YESBANK.NS:')
data = ticker.history(period='5d')
print(f'Data available: {not data.empty}')
if not data.empty:
    print(f'Latest price: Rs.{data["Close"].iloc[-1]:.2f}')
else:
    print('No data available')

# Test alternative symbols
alternative_symbols = ['YESBANK.BO', 'YESBANK', '532648.BO']
for symbol in alternative_symbols:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        if not data.empty:
            print(f'{symbol}: Rs.{data["Close"].iloc[-1]:.2f}')
        else:
            print(f'{symbol}: No data')
    except Exception as e:
        print(f'{symbol}: Error - {e}')
