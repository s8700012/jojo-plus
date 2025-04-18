# stock_selector.py
import requests
from bs4 import BeautifulSoup

def get_top_30_stocks():
    url = "https://example.com/preopen"  # 改成實際可用網站
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    stocks = []

    # 假設網站格式為表格：<tr><td>2330</td><td>台積電</td><td>成交量</td></tr>
    for row in soup.select('table tr')[1:]:  # 忽略標題
        cols = row.find_all('td')
        if len(cols) < 3:
            continue
        symbol = cols[0].text.strip()
        name = cols[1].text.strip()
        volume = int(cols[2].text.strip().replace(',', ''))

        if symbol in ['2330', '2317', '2454']:  # 排除權值股
            continue

        stocks.append({"symbol": symbol, "name": name, "volume": volume})

    # 按照成交量排序，取前30名
    sorted_stocks = sorted(stocks, key=lambda x: x["volume"], reverse=True)
    return sorted_stocks[:30]
