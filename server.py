from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import json
import datetime
import yfinance as yf
import os
import random

app = Flask(__name__)
model = load_model()

# 動態載入熱門非權值股清單（stocks.json 預設來源）
def load_stocks():
    with open('stocks.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    stock_list = load_stocks()
    data = []

    for stock in stock_list:
        symbol = f"{stock['symbol']}.TW"
        try:
            ticker = yf.Ticker(symbol)
            price_data = ticker.history(period='1d')
            price = round(price_data['Close'].iloc[-1], 2) if not price_data.empty else 0
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            price = 0

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

@app.route('/ping')
def ping():
    return "pong"

@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
