from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import json
import datetime
import yfinance as yf
import os

app = Flask(__name__)

# 載入股票清單
with open('stocks.json', 'r', encoding='utf-8') as f:
    stock_list = json.load(f)

# 載入 AI 模型
model = load_model()

# 建立報價快取字典
price_cache = {}

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    data = []
    now = datetime.datetime.now()

    for stock in stock_list:
        symbol = f"{stock['symbol']}.TW"
        cache_key = symbol

        # 快取：只更新超過1秒的報價
        if cache_key in price_cache and (now - price_cache[cache_key]['time']).seconds < 1:
            price = price_cache[cache_key]['price']
        else:
            try:
                ticker = yf.Ticker(symbol)
                history = ticker.history(period='1d')
                if history.empty:
                    raise ValueError("歷史資料為空")
                price = round(history['Close'].iloc[-1], 2)
                price_cache[cache_key] = {'price': price, 'time': now}
            except Exception as e:
                print(f"[錯誤] 無法抓取 {symbol} 報價：{e}")
                continue  # 出錯就跳過該標的

        # 跳過價格為 0 的標的
        if price == 0
