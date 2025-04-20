from flask import Flask, jsonify, send_file
import requests
from proxy_scraper import get_price
import json

app = Flask(__name__)

with open("stocks.json", "r", encoding="utf-8") as f:
    stocks = json.load(f)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/stocks")
def stock_data():
    result = []
    for stock in stocks:
        try:
            price = get_price(stock["symbol"])
            result.append({
                "代號": stock["symbol"],
                "名稱": stock["name"],
                "目前股價": price,
                "建議方向": "做多" if price > 50 else "觀望",
                "建議進場價": round(price * 0.99, 2),
                "建議出場價": round(price * 1.01, 2),
                "AI勝率": f"{50 + int(price) % 50}%"
            })
        except Exception as e:
            print(f"[錯誤] {stock['symbol']} 抓價失敗: {e}")
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
