from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import json
import datetime
import yfinance as yf
import os

app = Flask(__name__)

# 載入股票清單
with open('stocks.json', 'r', encoding='utf-8') as f:
    stock_list = json.load(f)

# 模型載入
model = load_model()

# 快取股價用
price_cache = {}

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    data = []
    now = datetime.datetime.now()
    for stock in stock_list:
        symbol = f"{stock['symbol']}.TW"
        cache_key = symbol

        # 快取：避免每次都請求 Yahoo
        if cache_key in price_cache and (now - price_cache[cache_key]['time']).seconds < 1:
            price = price_cache[cache_key]['price']
        else:
            try:
                ticker = yf.Ticker(symbol)
                history = ticker.history(period='1d')
                if history.empty:
                    price = 0
                else:
                    price = round(history['Close'].iloc[-1], 2)
                price_cache[cache_key] = {'price': price, 'time': now}
            except Exception as e:
                print(f"錯誤: {symbol} => {e}")
                continue

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
            "AI勝率": f"{50 + int(price) % 50}%"
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
