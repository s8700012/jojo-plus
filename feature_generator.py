import numpy as np
import pandas as pd
import yfinance as yf

def generate_features(symbol):
    symbol = f"{symbol}.TW"
    df = yf.download(symbol, period="5d", interval="1m", progress=False)
    
    if df.empty or len(df) < 20:
        return {}

    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['EMA5'] = df['Close'].ewm(span=5, adjust=False).mean()
    df['RSI'] = compute_rsi(df['Close'], 14)
    df['Volume_MA5'] = df['Volume'].rolling(window=5).mean()
    df['Price_Change'] = df['Close'].pct_change().fillna(0)

    latest = df.iloc[-1]
    features = {
        "price": round(latest['Close'], 2),
        "ma5": round(latest['MA5'], 2),
        "ma10": round(latest['MA10'], 2),
        "ema5": round(latest['EMA5'], 2),
        "rsi": round(latest['RSI'], 2),
        "volume_ma5": int(latest['Volume_MA5']),
        "price_change": round(latest['Price_Change'], 4)
    }
    return features

def compute_rsi(series, period):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi
