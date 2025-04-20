import requests
from bs4 import BeautifulSoup
import time

cache = {}

def get_price(symbol):
    url = f"https://tw.stock.yahoo.com/quote/{symbol}.TW"
    now = time.time()

    if symbol in cache and now - cache[symbol]["time"] < 3:
        return cache[symbol]["price"]

    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers, timeout=5)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
    if not tag or not tag.text:
        raise ValueError("找不到價格")
    price = float(tag.text.replace(",", ""))
    cache[symbol] = {"price": price, "time": now}
    return price
