import requests
import pandas as pd
from bs4 import BeautifulSoup

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
            # 排除權值股（如台積電 2330、鴻海 2317）
            if symbol not in ['2330', '2317'] and volume > 0:
                data.append({'symbol': symbol, 'name': name, 'volume': volume})
        except:
            continue

    df = pd.DataFrame(data)
    df = df.sort_values(by='volume', ascending=False).head(30)
    result = df[['symbol', 'name']].to_dict(orient='records')
    return result
