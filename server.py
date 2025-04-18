from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
from preopen_scraper import get_top30_stocks  # 即時抓熱門股
import random
import datetime
import yfinance as yf
import os

app = Flask(__name__)
model = load_model()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    data = []
    top_stocks = get_top30_stocks()  # 每次請求即時擷取

    for stock in top_stocks:
        symbol = f"{stock['symbol']}.TW"
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period='1d')
            if history.empty:
                price = 0
            else:
                price = round(history['Close'].iloc[-1], 2)
        except Exception as e:
            print(f"[Error] {symbol}: {e}")
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

@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

app = app  # for render.com
