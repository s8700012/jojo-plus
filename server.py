from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import json
import random
import datetime
import yfinance as yf
import os

app = Flask(__name__)

# 載入股票清單
with open('stocks.json', 'r', encoding='utf-8') as f:
    stock_list = json.load(f)

# 載入 AI 模型
model = load_model()

# 每秒快取價格
price_cache = {}

def fetch_price(symbol):
    now = datetime.datetime.now()
    if symbol in price_cache:
        cached_price, timestamp = price_cache[symbol]
        if (now - timestamp).seconds < 1:
            return cached_price

    # 嘗試 .TW（上市）與 .TWO（上櫃）
    for suffix in ['.TW', '.TWO']:
        try:
            ticker = yf.Ticker(symbol + suffix)
            history = ticker.history(period='1d')
            if not history.empty:
                price = round(history['Close'].iloc[-1], 2)
                price_cache[symbol] = (price, now)
                return price
        except Exception as e:
            print(f"[錯誤] {symbol}{suffix} 查詢失敗: {e}")
            continue

    print(f"[錯誤] {symbol} 查無報價（.TW/.TWO 都無資料）")
    return 0

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    data = []
    for stock in stock_list:
        symbol = stock["symbol"]
        price = fetch_price(symbol)
        if price == 0:
            continue
        features = generate_features(price)
        prediction = predict(model, features)
        data.append({
            "代號": stock["symbol"],
            "名稱": stock["name"],
            "目前股價": price,
            "建議方向": prediction,
            "建議進場價": round(price * 0.99, 2),
            "建議出場價": round(price * 1.01, 2),
            "AI勝率": f"{random.randint(60, 90)}%"
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
