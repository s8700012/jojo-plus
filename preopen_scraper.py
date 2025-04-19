import requests
from bs4 import BeautifulSoup
import datetime
import json

def fetch_preopen_stocks():
    url = "https://tw.stock.yahoo.com/rank/pre-volume"  # 模擬來源（需換為真實盤前來源）
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    symbols = []
    rows = soup.select('table tbody tr')
    for row in rows:
        cols = row.text.split()
        if len(cols) >= 2:
            symbol = cols[0]
            name = cols[1]
            if not symbol.startswith("00"):  # 過濾權值股（簡單判斷）
                symbols.append({"symbol": symbol, "name": name})
        if len(symbols) >= 30:
            break

    with open('stocks.json', 'w', encoding='utf-8') as f:
        json.dump(symbols, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    now = datetime.datetime.now().time()
    if datetime.time(8, 50) <= now <= datetime.time(9, 3):
        fetch_preopen_stocks()
