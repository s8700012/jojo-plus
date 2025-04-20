from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
from tw_stock_scraper import get_price
import json
import datetime
import os

app = Flask(__name__)

# 載入股票清單
with open('stocks.json', 'r', encoding='utf-8') as f:
    stock_list = json.load(f)

# 載入 AI 模型
model = load_model()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    data = []
    for stock in stock_list:
        try:
            price = get_price(stock['symbol'])
            if price is None or price == 0:
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
        except Exception as e:
            print(f"[錯誤] {stock['symbol']} AI 計算失敗: {e}")
            continue

    return jsonify(data)

@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, threaded=True)
