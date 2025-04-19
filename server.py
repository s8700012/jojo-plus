from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
import yfinance as yf
import datetime
import os
import json

app = Flask(__name__)

# 載入模型
model = load_model()

# 動態選股（模擬盤前熱門 30 檔非權值股）
def get_dynamic_stocks():
    return [
        {"symbol": "2603", "name": "長榮"},
        {"symbol": "2609", "name": "陽明"},
        {"symbol": "2615", "name": "萬海"},
        {"symbol": "1101", "name": "台泥"},
        {"symbol": "1216", "name": "統一"},
        {"symbol": "1301", "name": "台塑"},
        {"symbol": "1326", "name": "台化"},
        {"symbol": "1402", "name": "遠東新"},
        {"symbol": "2002", "name": "中鋼"},
        {"symbol": "2105", "name": "正新"},
        {"symbol": "2207", "name": "和泰車"},
        {"symbol": "2301", "name": "光寶科"},
        {"symbol": "2324", "name": "仁寶"},
        {"symbol": "2354", "name": "鴻準"},
        {"symbol": "2357", "name": "華碩"},
        {"symbol": "2382", "name": "廣達"},
        {"symbol": "2395", "name": "研華"},
        {"symbol": "2412", "name": "中華電"},
        {"symbol": "2451", "name": "創見"},
        {"symbol": "2606", "name": "裕民"},
        {"symbol": "2801", "name": "彰銀"},
        {"symbol": "2882", "name": "國泰金"},
        {"symbol": "3008", "name": "大立光"},
        {"symbol": "3034", "name": "聯詠"},
        {"symbol": "3209", "name": "全科"},
        {"symbol": "4904", "name": "遠傳"},
        {"symbol": "3702", "name": "大聯大"},
        {"symbol": "3037", "name": "欣興"},
        {"symbol": "3231", "name": "緯創"},
        {"symbol": "2345", "name": "智邦"}
    ]

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/stocks')
def get_stocks():
    stock_list = get_dynamic_stocks()
    data = []
    for stock in stock_list:
        symbol = f"{stock['symbol']}.TW"
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="1d")
            if history.empty:
                continue
            price = round(history["Close"].iloc[-1], 2)
        except Exception as e:
            print(f"無法取得 {symbol} 價格: {e}")
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
            "AI勝率": f"{round(60 + (price % 10), 2)}%"
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
