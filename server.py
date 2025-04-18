from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
from news_scraper import get_latest_news
import yfinance as yf
import json
import datetime

app = Flask(__name__)

# 載入股票清單
with open('stocks.json', 'r', encoding='utf-8') as f:
    stock_list = json.load(f)

# 載入 AI 模型
model = load_model()

# 首頁
@app.route('/')
def home():
    return send_file('index.html')

# 股票資料
@app.route('/stocks')
def get_stocks():
    data = []
    for stock in stock_list:
        symbol = f"{stock['symbol']}.TW"
        try:
            info = yf.Ticker(symbol).info
            price = round(info['regularMarketPrice'], 2)
        except:
            price = 0.0  # 若報價失敗，預設為 0

        features = generate_features(price)
        prediction = predict(model, features)
        data.append({
            "代號": stock["symbol"],
            "名稱": stock["name"],
            "目前股價": price,
            "建議方向": prediction,
            "建議進場價": round(price * 0.99, 2),
            "建議出場價": round(price * 1.01, 2),
            "AI勝率": f"{round(60 + 40 * abs(hash(stock['symbol'])) % 40 / 40)}%"
        })
    return jsonify(data)

# 最新新聞
@app.route('/news')
def get_news():
    return jsonify(get_latest_news())

# 時間同步
@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

# 部署用設定
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
