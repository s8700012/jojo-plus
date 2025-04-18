import requests
from bs4 import BeautifulSoup
import json

def fetch_preopen_stocks():
    url = "https://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html"  # 盤前撮合頁（模擬）
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 模擬解析邏輯：實際需調整為該頁實際結構
    rows = soup.select("table tbody tr")

    result = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 5:
            try:
                symbol = cols[0].text.strip()
                name = cols[1].text.strip()
                volume = int(cols[2].text.strip().replace(',', ''))
                if volume > 500:  # 成交量大於 500 視為熱門（可調整）
                    result.append({"symbol": symbol, "name": name})
            except:
                continue

    # 儲存前 30 檔非權值股
    filtered = result[:30]
    with open("stocks.json", "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    return filtered

if __name__ == "__main__":
    fetched = fetch_preopen_stocks()
    print("已更新熱門股票至 stocks.json")
