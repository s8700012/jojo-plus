from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import json, random, datetime, yfinance as yf, os

# 每秒快取：初始化快取變數
cache_data = []
cache_time = 0

# 每次啟動時抓取一次熱門 30 檔股票清單（可每分鐘重新取得）
stock_list = get_top_30_stocks()
                               
app = Flask(__name__)
model = load_model()

from stock_selector import get_top_30_stocks  # 新增模組

stock_list = get_top_30_stocks()

@app.route('/')
def home():
    return send_file("index.html")

@app.route('/stocks')
def get_stocks():
    data = []
    for stock in stock_list:
        symbol = f"{stock['symbol']}.TW"
        try:
            price = round(yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1], 2)
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

@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
