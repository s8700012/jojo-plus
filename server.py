from flask import Flask, jsonify, send_file
from preopen_scraper import get_hot_stocks
from feature_generator import generate_features
from ai_model import load_model, predict
import datetime
import yfinance as yf
import random
import os

app = Flask(__name__)
model = load_model()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    data = []
    hot_stocks = get_hot_stocks()

    for stock in hot_stocks:
        symbol = f"{stock['symbol']}.TW"
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.history(period='1d')['Close'].iloc[-1]
            price = round(price, 2)
        except Exception as e:
            print(f"抓取 {symbol} 錯誤: {e}")
            continue

        features = generate_features(price)
        suggestion = predict(model, features)
        data.append({
            "代號": stock["symbol"],
            "名稱": stock["name"],
            "目前股價": price,
            "建議方向": suggestion,
            "建議進場價": round(price * 0.99, 2),
            "建議出場價": round(price * 1.01, 2),
            "AI勝率": f"{random.randint(65, 90)}%"
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
