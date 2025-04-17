from flask import Flask, send_file, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # 預設 10000，Render 自動分配
    app.run(host='0.0.0.0', port=port)
