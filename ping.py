
import time
import requests

def keep_awake():
    url = "https://jojo-plus.onrender.com"  # 修改成你的 Render 網址
    while True:
        try:
            requests.get(url)
        except:
            pass
        time.sleep(600)  # 每 10 分鐘 Ping 一次
