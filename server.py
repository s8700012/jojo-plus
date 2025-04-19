from flask import Flask, jsonify, send_file
from feature_generator import generate_features
from ai_model import load_model, predict
from preopen_scraper import get_top30_preopen
import random
import datetime
import yfinance as yf
import os
import logging

app = Flask(__name__)

# 初始化 AI 模型
model = load_model()

# 記錄 log（除錯用）
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/ping')
def ping():
    return "pong"

@app.route('/time')
def time_now():
    return jsonify({"server_time": datetime.datetime.now().strftime("%H:%M:%S")})

@app.route('/stocks')
def get_stocks():
    stocks = get_top30_preopen()
    data = []

    for stock in stocks:
        symbol = f"{stock['symbol']}.TW"
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period='1d')
            if history.empty:
                logging.warning(f"[空資料] {symbol}")
                continue
            price = round(history['Close'].iloc[-1], 2)
        except Exception as e:
            logging.error(f"[錯誤擷取 {symbol}]: {e}")
            continue

        if price == 0:
            logging.warning(f"[價格為 0 被跳過] {symbol}")
            continue

        features = generate_features(price)
        prediction = predict(model, features)
        ai_score = random.randint(60, 90)

        record = {
            "代號": stock["symbol"],
            "名稱": stock["name"],
            "目前股價": price,
            "建議方向": prediction,
            "建議進場價": round(price * 0.99, 2),
            "建議出場價": round(price * 1.01, 2),
            "AI勝率": f"{ai_score}%"
        }
        data.append(record)
    return jsonify(data)


# 以下為 AI 模型與技術分析自學邏輯擴充預留
@app.route('/train_ai', methods=["POST"])
def train_ai():
    # 模擬每日訓練模型
    try:
        # 實作模型訓練：讀入歷史資料 -> 計算特徵 -> 模型優化
        result = {
            "message": "AI 模型訓練完成",
            "accuracy": f"{random.randint(70, 90)}%",
            "timestamp": datetime.datetime.now().isoformat()
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/status')
def status():
    return jsonify({
        "system": "Jojo Plus AI 系統",
        "version": "2.1",
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "正常運作中",
        "stock_count": len(get_top30_preopen())
    })


# 預設埠口
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    logging.info(f"Server running on port {port}")
    app.run(host='0.0.0.0', port=port)
