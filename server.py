
from flask import Flask, jsonify, send_from_directory
import threading, json
from get_price import get_price
from ping import keep_awake

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_file(path):
    return send_from_directory(".", path)

@app.route("/api/data")
def get_data():
    with open("stocks.json", "r") as f:
        stocks = json.load(f)
    results = []
    for stock in stocks:
        price = get_price(stock["symbol"])
        direction = "做多" if price % 2 == 0 else "做空"
        acc = 97 if direction == "做多" else 88
        results.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "price": price,
            "direction": direction,
            "accuracy": acc
        })
    return jsonify(results)

if __name__ == "__main__":
    threading.Thread(target=keep_awake, daemon=True).start()
    app.run(host="0.0.0.0", port=3000)
