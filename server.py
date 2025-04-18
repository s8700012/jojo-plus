# Flask 主程式
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return 'Jojo Plus 啟動成功'

if __name__ == '__main__':
    app.run()