
import yfinance as yf
def get_price(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval="1m")
    if not data.empty:
        return float(data["Close"].iloc[-1])
    return 0.0
