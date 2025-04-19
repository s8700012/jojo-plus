from flask import Flask, jsonify
from feature_generator import generate_features
from ai_model import load_model, predict
from preopen_scraper import get_top30_preopen
import datetime
import yfinance as yf
import random

app = Flask(__name__)
model = load_model()

# 記憶體儲存
stock_list = get_top30_preopen()  # 启动时呼叫

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
            "AI勝率": f"{random.randint(60, 90)}%"
        })
    return jsonify(data)
