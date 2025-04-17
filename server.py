from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/prices')
def prices():
    data = [
        {"symbol": "2330.TW", "name": "台積電", "price": 847.00, "direction": "做多", "probability": 97},
        {"symbol": "2317.TW", "name": "鴻海", "price": 134.50, "direction": "做空", "probability": 88},
        {"symbol": "1301.TW", "name": "台塑", "price": 35.50, "direction": "做空", "probability": 74},
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
