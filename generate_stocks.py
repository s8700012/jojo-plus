import requests
from bs4 import BeautifulSoup
import json
import re

def fetch_top_30_stocks():
    url = 'https://example.com/preopen'  # 請替換為正確盤前試撮網址
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    table = soup.find('table')  # 假設是第一個表格
    rows = table.find_all('tr')[1:]  # 排除表頭

    selected = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 5:
            symbol = cols[0].text.strip()
            name = cols[1].text.strip()
            volume = int(cols[4].text.replace(',', ''))
            if not symbol.startswith('00'):  # 範例：排除權值股
                selected.append((symbol, name, volume))

    selected.sort(key=lambda x: x[2], reverse=True)
    top_30 = [{"symbol": x[0], "name": x[1]} for x in selected[:30]]

    with open('stocks.json', 'w', encoding='utf-8') as f:
        json.dump(top_30, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    fetch_top_30_stocks()
