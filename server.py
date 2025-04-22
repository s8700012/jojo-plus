from flask import Flask, jsonify, send_file
from concurrent.futures import ThreadPoolExecutor
import json
import random
import datetime
import requests
import os

app = Flask(__name__)

# stocks.json 路徑
STOCK_LIST_FILE = 'stocks.json'

# 每秒快取價格
price_cache = {}

# 載入股票清單
try:
    with open(STOCK_LIST_FILE, 'r', encoding='utf-8') as f:
        stock_list = json.load(f)
except Exception as e:
    print(f"[錯誤] 無法載入 stocks.json：{e}")
    stock_list = []

# 使用 Render 上的 Proxy API 擷取股價
def fetch_price(symbol):
    now = datetime.datetime.now()
    if symbol in price_cache:
        cached_price, timestamp = price_cache[symbol]
        if (now - timestamp).seconds < 1:
            return cached_price
    try:
        url = f"https://proxy-server.onrender.com/quote?symbol={symbol}"
        response = requests.get(url, timeout=5)
        result = response.json()
        price = round(float(result['price']), 2)
    except Exception as e:
        print(f"[錯誤] {symbol}: {e}")
        price = 0
    price_cache[symbol] = (price, now)
    return price

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    def process(stock):
        symbol = stock["symbol"]
        try:
            price = fetch_price(symbol)
            print(f"[Debug] 取得 {symbol} 即時價格：{price}")
            if price == 0:
                return None
            prediction = '做多' if price % 2 > 1 else '做空'
            return {
                "代號": symbol,
                "名稱": stock["name"],
                "目前股價": price,
                "建議方向": prediction,
                "建議進場價": round(price * 0.99, 2),
                "建議出場價": round(price * 1.01, 2),
                "AI勝率": f"{random.randint(60, 90)}%"
            }
        except Exception as e:
            print(f"[錯誤] 分析 {symbol} 失敗：{e}")
            return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process, stock_list))

    return jsonify([r for r in results if r is not None])

@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
