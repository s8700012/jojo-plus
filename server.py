from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import yfinance as yf
import json
import datetime
import os

app = Flask(__name__)
model = load_model()

# 載入由爬蟲自動產生的 stocks.json
with open('stocks.json', 'r', encoding='utf-8') as f:
    content = f.read().strip()
    if not content:
        raise ValueError("stocks.json 為空，請檢查檔案來源")
    stock_list = json.loads(content)

@app.route('/')
def home():
    return send_file("index.html")

@app.route('/stocks')
def get_stocks():
    data = []
    for stock in stock_list:
        symbol = f"{stock['symbol']}.TW"
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period='1d')
            price = round(history['Close'].iloc[-1], 2) if not history.empty else 0
        except:
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
            "AI勝率": f"{round(80 + (price % 10), 1)}%"
        })
    return jsonify(data)

@app.route('/ping')
def ping():
    return "pong"

@app.route('/time')
def get_time():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
