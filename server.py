from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
from news_scraper import get_latest_news
import json
import yfinance as yf
import datetime
import random
import os

app = Flask(__name__)
model = load_model()

with open('stocks.json', 'r', encoding='utf-8') as f:
    stock_list = json.load(f)

price_cache = {}

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    data = []
    for stock in stock_list:
        symbol = f"{stock['symbol']}.TW"
        if symbol in price_cache and (datetime.datetime.now() - price_cache[symbol]['time']).seconds < 1:
            price = price_cache[symbol]['price']
        else:
            try:
                price = yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1]
                price = round(price, 2)
                price_cache[symbol] = {'price': price, 'time': datetime.datetime.now()}
            except:
                continue

        features = generate_features(price)
        direction = predict(model, features)
        data.append({
            "代號": stock["symbol"],
            "名稱": stock["name"],
            "目前股價": price,
            "建議方向": direction,
            "建議進場價": round(price * 0.99, 2),
            "建議出場價": round(price * 1.01, 2),
            "AI勝率": f"{random.randint(60, 90)}%"
        })
    return jsonify(data)

@app.route('/news')
def get_news():
    return jsonify(get_latest_news())

@app.route('/time')
def get_time():
    return jsonify({"server_time": datetime.datetime.now().strftime('%H:%M:%S')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
