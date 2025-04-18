import requests
from bs4 import BeautifulSoup
import json
import datetime

# 排除的權值股代碼（可擴充）
EXCLUDE_SYMBOLS = {"2330", "2317", "2454", "2303", "2881", "2891"}

def fetch_top_volume_stocks():
    url = "https://tw.stock.yahoo.com/market/most-active"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select("table tbody tr")

        result = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 5:
                symbol = cols[0].text.strip().split(" ")[0]
                name = cols[0].text.strip().split(" ")[-1]
                if symbol not in EXCLUDE_SYMBOLS:
                    result.append({"symbol": symbol, "name": name})
                if len(result) == 30:
                    break
        return result

    except Exception as e:
        print("[Error] 無法取得熱門成交量股票：", e)
        return []

def save_to_stocks_json(stocks):
    with open("stocks.json", "w", encoding="utf-8") as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 擷取熱門股票中...")
    top_stocks = fetch_top_volume_stocks()
    if top_stocks:
        save_to_stocks_json(top_stocks)
        print(f"成功儲存 30 檔熱門股票到 stocks.json")
    else:
        print("擷取失敗")
def select_top_stocks():
    # 這裡放入你擷取盤前 08:50～09:00 的熱門成交量股票邏輯
    return [
        {"symbol": "2603", "name": "長榮"},
        {"symbol": "2609", "name": "陽明"},
        {"symbol": "2615", "name": "萬海"},
        # 最多回傳 30 檔（不含權值股）
    ]
