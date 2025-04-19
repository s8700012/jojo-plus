import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def fetch_preopen_stocks():
    url = "https://tw.stock.yahoo.com/rank/volume"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "html.parser")

        # 根據實際網頁結構選擇正確的 table selector
        table = soup.find("table")
        if not table:
            print("找不到成交量排行表格")
            return

        rows = table.find_all("tr")
        stock_data = []

        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) >= 5:
                symbol = cols[0].text.strip()
                name = cols[1].text.strip()
                volume_text = cols[4].text.strip().replace(",", "")
                try:
                    volume = int(volume_text)
                except ValueError:
                    continue

                if symbol and volume > 0:
                    stock_data.append({
                        "symbol": symbol,
                        "name": name,
                        "volume": volume
                    })

        # 排除權值股（例如台積電、鴻海等），這裡以股號作為範例
        exclude_symbols = {"2330", "2317"}
        filtered_stocks = [s for s in stock_data if s["symbol"] not in exclude_symbols]

        # 按照成交量排序，取前 30 檔
        top_stocks = sorted(filtered_stocks, key=lambda x: x["volume"], reverse=True)[:30]

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
