import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def fetch_top30_stocks():
    url = "https://www.twse.com.tw/zh/page/trading/idx/MI_5MINS_HOT.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find("table")
    if not table:
        return []

    rows = table.find_all("tr")[1:]
    stocks = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            symbol = cols[0].text.strip()
            name = cols[1].text.strip()
            if symbol.isdigit():
                stocks.append({"symbol": symbol, "name": name})
        if len(stocks) >= 30:
            break
    return stocks

if __name__ == "__main__":
    top_stocks = fetch_top30_stocks()
    with open("stocks.json", "w", encoding="utf-8") as f:
        json.dump(top_stocks, f, ensure_ascii=False, indent=2)
    print(f"[{datetime.now()}] 已儲存最新熱門 30 檔股票至 stocks.json")
