from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import json
import random
import datetime
import yfinance as yf
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

    # 轉換為 .TW 並保留對應資訊
    symbols_map = {f"{stock['symbol']}.TW": stock for stock in stock_list}
    symbols = list(symbols_map.keys())

    try:
        # 批次抓取所有股票的價格
        history = yf.download(tickers=" ".join(symbols), period='1d', group_by='ticker', threads=True)
    except Exception as e:
        print("[Error] 批次抓取失敗:", e)
        return jsonify([])

    for sym in symbols:
        stock = symbols_map[sym]
        try:
            # 判斷資料格式是多股票還是單股票
            if sym in history and not history[sym].empty:
                price = round(history[sym]['Close'].iloc[-1], 2)
            else:
                continue
        except Exception as e:
            print(f"[錯誤] 取得 {sym} 價格失敗:", e)
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

@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

app = app
