# 檔名：tw_stock_scraper.py
import requests
import time
import re
import json

price_cache = {}

def get_price(symbol):
    full_symbol = f"{symbol}.TW"
    url = f"https://tw.stock.yahoo.com/quote/{symbol}.TW"
    now = time.time()

    # 快取機制：2秒內不重抓
    if full_symbol in price_cache and now - price_cache[full_symbol]["timestamp"] < 2:
        return price_cache[full_symbol]["price"]

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()

        # 擷取 JavaScript 內嵌 JSON
        match = re.search(r'root.App.main\s*=\s*({.*?});\n', res.text)
        if not match:
            print(f"[警告] {symbol} 找不到 root.App.main 資料")
            return None

        data = json.loads(match.group(1))

        # 安全擷取價格（避免 KeyError）
        price_data = data.get("context", {}).get("dispatcher", {}).get("stores", {}).get("QuoteSummaryStore", {}).get("price", {})
        if not price_data or "regularMarketPrice" not in price_data:
            print(f"[警告] {symbol} 找不到 regularMarketPrice")
            return None

        price = price_data["regularMarketPrice"]["raw"]
        price_cache[full_symbol] = {"price": price, "timestamp": now}
        return float(price)

    except Exception as e:
        print(f"[爬蟲錯誤] {symbol}: {e}")
        return None
