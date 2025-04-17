# Flask server with real-time stock data
from flask import Flask, render_template, jsonify
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api/data')
def data():
    return jsonify({'price': 100, 'signal': 'buy'})
if __name__ == '__main__':
    app.run(debug=True, port=3000)