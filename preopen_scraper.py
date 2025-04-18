# fetch_preopen_data.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import datetime

def fetch_preopen_data():
    url = 'https://www.twse.com.tw/zh/page/trading/pre_trading/pre_MktCap.html'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
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
            if volume > 0:
                data.append({'symbol': symbol, 'name': name, 'volume': volume})
        except:
            continue

    if not data:
        print("未擷取到任何有效資料")
        return

    df = pd.DataFrame(data)
    df = df.sort_values(by='volume', ascending=False).head(30)

    with open('stocks.json', 'w', encoding='utf-8') as f:
        json.dump(df[['symbol', 'name']].to_dict(orient='records'), f, ensure_ascii=False, indent=2)

    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 已成功寫入 stocks.json，總計 {len(df)} 檔")

if __name__ == "__main__":
    fetch_preopen_data()
