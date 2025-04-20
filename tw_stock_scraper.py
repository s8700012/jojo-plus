import requests
import time

price_cache = {}
PROXY_URL = "https://yahoo-proxy-server.s8700012.repl.co"

def get_price(symbol):
    now = time.time()

    # 快取：兩秒內不重抓
    if symbol in price_cache and now - price_cache[symbol]["timestamp"] < 2:
        return price_cache[symbol]["price"]

    try:
        url = f"{PROXY_URL}/quote?symbol={symbol}"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()

        price = data.get("price")
        if price is not None:
            price_cache[symbol] = {"price": price, "timestamp": now}
            print(f"[DEBUG] {symbol} - 從 Proxy 抓到價格: {price}")
            return price
        else:
            print(f"[警告] {symbol} - Proxy 未回傳價格")
            return None

    except Exception as e:
        print(f"[錯誤] {symbol} Proxy 擷取失敗: {e}")
        return None
