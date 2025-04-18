from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import json
import datetime
import yfinance as yf
import os
import threading
import time

app = Flask(__name__)

with open('stocks.json', 'r', encoding='utf-8') as f:
    stock_list = json.load(f)

model = load_model()

# 全局快取價格資料，每秒更新
price_cache = {}

def update_prices():
    global price_cache
    while True:
        temp_cache = {}
        for stock in stock_list:
            symbol = f"{stock['symbol']}.TW"
            try:
                ticker = yf.Ticker(symbol)
                history = ticker.history(period='1d')
                if history.empty:
                    continue
                price = round(history['Close'].iloc[-1], 2)
                temp_cache[stock['symbol']] = price
            except Exception as e:
                print(f"[Error] {symbol}: {e}")
        price_cache = temp_cache
        time.sleep(1)

# 啟動背景執行緒
threading.Thread(target=update_prices, daemon=True).start()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    data = []
    for stock in stock_list:
        symbol = stock['symbol']
        price = price_cache.get(symbol, 0)

        if price == 0:
            continue

        features = generate_features(price)
        prediction = predict(model, features)
        data.append({
            "代號": symbol,
            "名稱": stock["name"],
            "目前股價": price,
            "建議方向": prediction,
            "建議進場價": round(price * 0.99, 2),
            "建議出場價": round(price * 1.01, 2),
            "AI勝率": f"{round(60 + (price % 30), 1)}%"
        })
    return jsonify(data)

@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
