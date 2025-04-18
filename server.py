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
    app.run(debug=True, port=3000)

