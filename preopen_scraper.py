import requests
import json

def fetch_preopen_stocks():
    url = 'https://example.com/api/preopen'  # 改為真實盤前 API
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        # 篩選熱門非權值股邏輯（示範）
        filtered = []
        for item in data:
            if item['symbol'] not in ['2330', '2317']:  # 排除權值股
                filtered.append({
                    "symbol": item["symbol"],
                    "name": item["name"]
                })
            if len(filtered) == 30:
                break

        # 寫入 stocks.json
        if filtered:
            with open("stocks.json", "w", encoding="utf-8") as f:
                json.dump(filtered, f, ensure_ascii=False, indent=2)
            print("成功寫入 stocks.json，共", len(filtered), "檔")
        else:
            print("無熱門股票資料")

    except Exception as e:
        print("發生錯誤：", e)

if __name__ == "__main__":
    fetch_preopen_stocks()
