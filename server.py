from flask import Flask, send_file, send_from_directory

app = Flask(__name__)

# 首頁路由，直接送出 main 目錄下的 index.html
@app.route('/')
def home():
    return send_file('index.html')

# 其他靜態檔案路由（像是 .js, .css）
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# 主程式啟動，重要：host 必須為 0.0.0.0，port 可為 3000 或 Render 指定的
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
