from flask import Flask, jsonify, send_from_directory
import random
app = Flask(__name__)
@app.route('/')
def index(): return send_from_directory('.', 'index.html')
@app.route('/<path:path>')
def static_files(path): return send_from_directory('.', path)
@app.route('/data')
def data():
 return jsonify([
  {'symbol':'2330.TW','name':'台積電','price':851,'direction':'做多','entry':850,'exit':860,'winrate':93},
  {'symbol':'2317.TW','name':'鴻海','price':135.5,'direction':'做空','entry':135,'exit':130,'winrate':85}
])