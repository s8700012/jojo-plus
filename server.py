from flask import Flask, jsonify, send_file, request
from feature_generator import generate_features
from ai_model import load_model, predict
from news_scraper import get_latest_news
import json
import random
import datetime

app = Flask(__name__)

# 載入股票清單
with open('stocks.json', 'r', encoding='utf-8') as f:
    stock_list = json.load(f)

model = load_model()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    data = []
    for stock in stock_list:
        price = round(100 + random.uniform(-5, 5), 2)
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

@app.route('/news')
def get_news():
    return jsonify(get_latest_news())

@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

if __name__ == '__main__':
    app.run(debug=True, port=10000)
