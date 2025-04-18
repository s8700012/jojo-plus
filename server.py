from flask import Flask, send_file, send_from_directory, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/stocks')
def get_stocks():
    with open('stocks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=3000)