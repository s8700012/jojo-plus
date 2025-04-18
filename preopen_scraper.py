import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def fetch_preopen_data():
    url = 'https://example.com/preopen'  # 更換為實際的盤前試撮來源網址
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    for row in soup.select('table tr'):
        cols = row.find_all('td')
        if len(cols) < 5:
            continue
        time_str = cols[0].text.strip()
        symbol = cols[1].text.strip()
        volume = int(cols[4].text.strip().replace(',', ''))
        time = datetime.strptime(time_str, '%H:%M:%S')
        data.append({
            'time': time,
            'symbol': symbol,
            'volume': volume
        })
    df = pd.DataFrame(data)
    df.to_csv('preopen_volume.csv', index=False)

if __name__ == "__main__":
    fetch_preopen_data()
