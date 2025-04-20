
import requests
from bs4 import BeautifulSoup
import time

# 快取機制（避免每次都重抓）
price_cache = {}

def get_price(symbol):
    """
    從 Yahoo Finance 擷取即時價格，symbol 為 '2330'（會轉成 2330.TW）
    """
    full_symbol = f"{symbol}.TW"
    url = f"https://tw.stock.yahoo.com/quote/{symbol}.TW"

    now = time.time()
    # 如果快取在 2 秒內，直接返回
    if full_symbol in price_cache and now - price_cache[full_symbol]["timestamp"] < 2:
        return price_cache[full_symbol]["price"]

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
        if tag:
            price = float(tag.text.replace(",", ""))
            # 更新快取
            price_cache[full_symbol] = {"price": price, "timestamp": now}
            return price
    except Exception as e:
        print(f"[爬蟲錯誤] {symbol}: {e}")
        return None
