import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

def fetch_preopen_data():
    url = 'https://www.twse.com.tw/zh/page/trading/pre_trading/pre_MktCap.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    for row in soup.select('table tr')[1:]:
        cols = row.find_all('td')
        if len(cols) < 5:
            continue
        try:
            symbol = cols[0].text.strip()
            name = cols[1].text.strip()
            volume_text = cols[4].text.strip().replace(',', '').replace('--', '0')
            volume = int(volume_text)
            if volume > 0:  # 避免無效資料
                data.append({'symbol': symbol, 'name': name, 'volume': volume})
        except:
            continue

    df = pd.DataFrame(data)
    df = df.sort_values(by='volume', ascending=False).head(30)

    with open('stocks.json', 'w', encoding='utf-8') as f:
        json.dump(df[['symbol', 'name']].to_dict(orient='records'), f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_preopen_data()
