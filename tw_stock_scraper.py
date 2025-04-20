import requests
import time
import re
import json

price_cache = {}

def get_price(symbol):
    full_symbol = f"{symbol}.TW"
    url = f"https://tw.stock.yahoo.com/quote/{symbol}.TW"
    now = time.time()

    if full_symbol in price_cache and now - price_cache[full_symbol]['timestamp'] < 2:
        return price_cache[full_symbol]['price']

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()

        # 從 JavaScript <script> 中找出 JSON 嵌入價格
        match = re.search(r'root.App.main\s*=\s*({.*});', res.text)
        if match:
            data = json.loads(match.group(1))
            price = data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['regularMarketPrice']['raw']
            if price:
                price_cache[full_symbol] = {"price": price, "timestamp": now}
                return float(price)

        print(f"[警告] {symbol} 無法從 script 中擷取報價")
        return None

    except Exception as e:
        print(f"[爬蟲錯誤] {symbol}: {e}")
        return None
