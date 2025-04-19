import requests
from bs4 import BeautifulSoup
import json

exclude_list = {"2330", "2317", "2454", "2303", "2881", "2882"}

def fetch_preopen_stocks():
    url = "https://www.twse.com.tw/zh/page/trading/pretrading/stock.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    simulated_data = [
        {"symbol": "2603", "name": "長榮", "volume": 5000},
        {"symbol": "2609", "name": "陽明", "volume": 4500},
        {"symbol": "2615", "name": "萬海", "volume": 4300},
        {"symbol": "2301", "name": "光寶科", "volume": 4200},
        {"symbol": "2324", "name": "仁寶", "volume": 4100},
    ]

    top_stocks = [
        stock for stock in simulated_data if stock["symbol"] not in exclude_list
    ]
    top_stocks = sorted(top_stocks, key=lambda x: x["volume"], reverse=True)[:30]

    with open("stocks.json", "w", encoding="utf-8") as f:
        json.dump([{"symbol": s["symbol"], "name": s["name"]} for s in top_stocks], f, ensure_ascii=False, indent=2)

    print("已更新 stocks.json，範例第一檔：", top_stocks[0])

if __name__ == "__main__":
    fetch_preopen_stocks()
