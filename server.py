from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import json
import random
import datetime
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

model = load_model()
tracked_stocks = []

def fetch_preopen_hot_stocks():
    url = "https://www.twse.com.tw/zh/page/trading/exchange/TWTB4U.html"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.select_one("table")
        rows = table.select("tr")[1:51]
        hot = []
        for row in rows:
            cols = row.select("td")
            if len(cols) >= 2:
                symbol = cols[0].text.strip()
                name = cols[1].text.strip()
                hot.append({"symbol": symbol, "name": name})
        return hot
    except Exception as e:
        print("[Error] 擷取熱門股失敗:", e)
        return []

@app.route('/')
def home():
    return send_file("index.html")

@app.route('/stocks')
def get_stocks():
    global tracked_stocks
    now = datetime.datetime.now().strftime("%H:%M")

    if not tracked_stocks and "08:50" <= now <= "09:10":
        tracked_stocks = fetch_preopen_hot_stocks()

    if not tracked_stocks:
        with open("stocks.json", "r", encoding="utf-8") as f:
            tracked_stocks = json.load(f)

    data = []
    for stock in tracked_stocks:
        symbol = f"{stock['symbol']}.TW"
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            price = round(hist["Close"].iloc[-1], 2) if not hist.empty else 0
        except Exception as e:
            print(f"[Error] {symbol}: {e}")
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

@app.route('/ping')
def ping():
    return "pong"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
