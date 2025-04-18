import requests
import pandas as pd
import json
from datetime import datetime

def fetch_top_stocks(limit=30):
    url = "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=&type=ALL"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        table = None

        # 找出正確的表格
        for item in data['data5']:
            if len(item) > 8:  # 避免空資料
                if not item[0].startswith("00"):  # 排除權值股可能條件，可依需求調整
                    if table is None:
                        table = []
                    table.append({
                        "symbol": item[0].strip(),
                        "name": item[1].strip(),
                        "volume": int(item[2].replace(",", ""))
                    })

        # 按照成交量排序
        sorted_stocks = sorted(table, key=lambda x: x['volume'], reverse=True)

        # 選出前 N 檔
        result = [{"symbol": stock["symbol"], "name": stock["name"]} for stock in sorted_stocks[:limit]]

        # 寫入 stocks.json
        with open("stocks.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 已更新前 {limit} 檔熱門股 stocks.json")

    except Exception as e:
        print(f"抓取資料錯誤: {e}")

if __name__ == "__main__":
    fetch_top_stocks()
