import requests
from bs4 import BeautifulSoup
import time

# 快取報價
price_cache = {}

def get_price(symbol):
    full_symbol = f"{symbol}.TW"
    url = f"https://tw.stock.yahoo.com/quote/{symbol}.TW"
    now = time.time()

    # 2 秒內使用快取
    if full_symbol in price_cache and now - price_cache[full_symbol]['timestamp'] < 2:
        return price_cache[full_symbol]['price']

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # 嘗試從 <fin-streamer> 擷取
        tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
        if not tag:
            # 備援：找有 aria-label 的價格文字
            alt_tag = soup.find("span", attrs={"class": "D(f) Ai(c) Mend(8px)"})
            if alt_tag:
                tag = alt_tag.find("span")
        
        if tag and tag.text:
            price = float(tag.text.replace(",", ""))
            price_cache[full_symbol] = {"price": price, "timestamp": now}
            return price

        print(f"[警告] 無法擷取 {symbol} 即時價格")
        return None

    except Exception as e:
        print(f"[爬蟲錯誤] {symbol}: {e}")
        return None
