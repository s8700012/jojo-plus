from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import json
import datetime
import yfinance as yf
import os
from apscheduler.schedulers.background import BackgroundScheduler
from stock_selector import update_hot_stocks

app = Flask(__name__)

# 初始化
model = load_model()

# 載入股票清單
def load_stocks():
    with open('stocks.json', 'r', encoding='utf-8') as f:
        return json.load(f)

stock_list = load_stocks()

# 每日自動更新熱門股清單
def daily_refresh():
    print("[系統] 自動更新 stocks.json 中...")
    update_hot_stocks()
    global stock_list
    stock_list = load_stocks()

# 安排每日早上 08:50 執行
scheduler = BackgroundScheduler()
scheduler.add_job(daily_refresh, 'cron', hour=8, minute=50)
scheduler.start()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    data = []
    for stock in stock_list:
        symbol = f"{stock['symbol']}.TW"
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period='1d')
            if history.empty:
                price = 0
            else:
                price = round(history['Close'].iloc[-1], 2)
        except Exception as e:
            print(f"[錯誤] {symbol}: {e}")
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
            "AI勝率": f"{prediction.count('多')*10 + 60}%"
        })
    return jsonify(data)

@app.route('/time')
def time_now
