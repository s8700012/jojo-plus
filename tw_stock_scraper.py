# 檔名：tw_stock_scraper.py
import requests
from bs4 import BeautifulSoup
import time

price_cache = {}

def get_price(symbol):
    full_symbol = f"{symbol}.TW"
    url = f"https://tw.stock.yahoo.com/quote/{symbol}.TW"
    now = time.time()

    # 快取：兩秒內不重抓
    if full_symbol in price_cache and now - price_cache[full_symbol]['timestamp'] < 2:
        return price_cache[full_symbol]['price']

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
        if tag and tag.text:
            price = float(tag.text.replace(",", ""))
            price_cache[full_symbol] = {"price": price, "timestamp": now}
            return price
        else:
            print(f"[警告] {symbol} 未抓到價格")
            return None

    except Exception as e:
        print(f"[爬蟲錯誤] {symbol}: {e}")
        return None
