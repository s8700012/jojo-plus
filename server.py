from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import json
import yfinance as yf
import datetime
import os
import threading
import time

app = Flask(__name__)

# 載入股票清單
with open('stocks.json', 'r', encoding='utf-8') as f:
    stock_list = json.load(f)

# 載入 AI 模型
model = load_model()

# 快取報價
price_cache = {}

def fetch_price_loop():
    while True:
        for stock in stock_list:
            symbol = f"{stock['symbol']}.TW"
            try:
                ticker = yf.Ticker(symbol)
                history = ticker.history(period='1d')
                if not history.empty:
                    price = round(history['Close'].iloc[-1], 2)
                    price_cache[stock['symbol']] = price
            except Exception as e:
                print(f"[Error] {symbol}: {e}")
        time.sleep(1)

# 啟動快取更新執行緒
threading.Thread(target=fetch_price_loop, daemon=True).start()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    data = []
    for stock in stock_list:
        symbol = stock['symbol']
        name = stock['name']
        price = price_cache.get(symbol, 0)
        if price == 0:
            continue
        features = generate_features(price)
        prediction = predict(model, features)
        data.append({
            "代號": symbol,
            "名稱": name,
            "目前股價": price,
            "建議方向": prediction,
            "建議進場價": round(price * 0.99, 2),
            "建議出場價": round(price * 1.01, 2),
            "AI勝率": f"{50 + (price % 50) // 2:.0f}%"
        })
    return jsonify(data)

@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
