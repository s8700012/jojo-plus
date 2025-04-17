import os
from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stocks')
def stocks():
    with open('stocks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)