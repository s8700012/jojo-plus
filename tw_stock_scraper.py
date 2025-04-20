import requests
import time
import re
import json

price_cache = {}

def get_price(symbol):
    full_symbol = f"{symbol}.TW"
    url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/QuoteService.getQuote?symbols={symbol}.TW"

    now = time.time()
    if full_symbol in price_cache and now - price_cache[full_symbol]['timestamp'] < 2:
        return price_cache[full_symbol]['price']

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
        data = res.json()

        if isinstance(data, list) and data[0].get("regularMarketPrice"):
            price = float(data[0]["regularMarketPrice"])
            price_cache[full_symbol] = {"price": price, "timestamp": now}
            return price
        else:
            print(f"[警告] {symbol} 無法取得 regularMarketPrice")
            return None
    except Exception as e:
        print(f"[爬蟲錯誤] {symbol}: {e}")
        return None
