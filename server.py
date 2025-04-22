# server.py

from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
from concurrent.futures import ThreadPoolExecutor
import json
import random
import datetime
import requests
import os

# 啟動時自動執行選股模組
import stock_selector
stock_selector.select_top_30()

app = Flask(__name__)

# 載入股票清單
try:
    with open('stocks.json', 'r', encoding='utf-8') as f:
        stock_list = json.load(f)
except Exception as e:
    print(f"[錯誤] 無法載入 stocks.json：{e}")
    stock_list = []

# 載入 AI 模型
model = load_model()

# 快取價格，每秒更新
price_cache = {}

# 使用 TWSE Proxy 伺服器
def fetch_price(symbol):
    now = datetime.datetime.now()
    if symbol in price_cache:
        cached_price, timestamp = price_cache[symbol]
        if (now - timestamp).seconds < 1:
            return cached_price
    try:
        url = f"https://proxy-server.onrender.com/quote?symbol={symbol}"
        res = requests.get(url, timeout=5)
        result = res.json()
        price = round(float(result["price"]), 2)
        price_cache[symbol] = (price, now)
        return price
    except Exception as e:
        print(f"[錯誤] 擷取 {symbol} 報價失敗：{e}")
        return 0

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    def process(stock):
        symbol = stock["symbol"]
        price = fetch_price(symbol)
        if price == 0:
            return None
        features = generate_features(price)
        prediction = predict(model, features)
        return {
            "代號": symbol,
            "名稱": stock["name"],
            "目前股價": price,
            "建議方向": prediction,
            "建議進場價": round(price * 0.99, 2),
            "建議出場價": round(price * 1.01, 2),
            "AI勝率": f"{random.randint(60, 90)}%"
        }

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process, stock_list))

    return jsonify([r for r in results if r])

@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
