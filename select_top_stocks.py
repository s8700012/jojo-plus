import requests
from bs4 import BeautifulSoup
import json

def fetch_top_30():
    url = "https://www.twse.com.tw/zh/page/trading/pretrading/stock.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table")

    if not table:
        return []

    rows = table.find_all("tr")[1:]
    results = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 10:
            continue
        symbol = cols[0].text.strip()
        name = cols[1].text.strip()
        vol = cols[6].text.replace(",", "")
        try:
            vol = int(vol)
            if not symbol.startswith("00") and not symbol.startswith("23"):  # 排除權值股
                results.append((symbol, name, vol))
        except:
            continue

    sorted_results = sorted(results, key=lambda x: x[2], reverse=True)
    top_30 = sorted_results[:30]
    return [{"symbol": x[0], "name": x[1]} for x in top_30]

def save_to_json():
    top_stocks = fetch_top_30()
    with open("stocks.json", "w", encoding="utf-8") as f:
        json.dump(top_stocks, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    save_to_json()
