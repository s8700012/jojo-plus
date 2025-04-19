import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

def fetch_preopen_stocks():
    url = "https://example.com/preopen"  # 替換為真實網址
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        table_rows = soup.select("table tr")
        stock_data = []

        for row in table_rows[1:]:
            cols = row.find_all("td")
            if len(cols) >= 5:
                symbol = cols[0].text.strip()
                name = cols[1].text.strip()
                volume = int(cols[4].text.replace(",", "").strip())

                if symbol and volume > 0:
                    stock_data.append({
                        "symbol": symbol,
                        "name": name,
                        "volume": volume
                    })

        # 按照成交量排序，取前 30 檔（可排除權值股）
        top_stocks = sorted(stock_data, key=lambda x: x["volume"], reverse=True)[:30]

        # 儲存為 stocks.json
        with open("stocks.json", "w", encoding="utf-8") as f:
            json.dump([{"symbol": s["symbol"], "name": s["name"]} for s in top_stocks], f, ensure_ascii=False, indent=2)

        print("stocks.json 更新完成，共擷取：", len(top_stocks), "檔")
    except Exception as e:
        print("擷取錯誤：", e)

if __name__ == "__main__":
    now = datetime.now().strftime("%H:%M:%S")
    print("執行時間：", now)
    fetch_preopen_stocks()
