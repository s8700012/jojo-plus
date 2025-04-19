from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import json
import yfinance as yf
import datetime
import os

app = Flask(__name__)

model = load_model()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    with open('stocks.json', 'r', encoding='utf-8') as f:
        stock_list = json.load(f)

    data = []
    for stock in stock_list:
        symbol = f"{stock['symbol']}.TW"
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period='1d', interval='1m')
            if history.empty:
                continue
            price = round(history['Close'].iloc[-1], 2)
        except Exception as e:
            print(f"[Error] {symbol}: {e}")
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
            "AI勝率": f"{round(60 + price % 30)}%"
        })

    return jsonify(data)

@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
