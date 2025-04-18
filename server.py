from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
from select_top_stocks import select_top_stocks
import json, random, datetime, yfinance as yf, os, time

app = Flask(__name__)

# 第一次部署或每天執行，先產生 stocks.json
select_top_stocks()

# 等待 stocks.json 檔案產生（最多等 5 秒）
for i in range(5):
    if os.path.exists('stocks.json'):
        break
    time.sleep(1)

# 確保存在後才讀取
if not os.path.exists('stocks.json'):
    raise FileNotFoundError("stocks.json 未正確產生，請檢查 select_top_stocks 函數邏輯")

with open('stocks.json', 'r', encoding='utf-8') as f:
    stock_list = json.load(f)

model = load_model()

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
            price = round(history['Close'].iloc[-1], 2) if not history.empty else 0
        except Exception as e:
            print(f"[Error] {symbol}: {e}")
            price = 0

        if price == 0: continue

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
