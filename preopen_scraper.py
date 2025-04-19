import requests
import pandas as pd
from datetime import datetime

def get_top30_preopen():
    date_str = datetime.now().strftime("%Y%m%d")
    url = f"https://www.twse.com.tw/rwd/zh/preop/preopQ?date={date_str}&response=json"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"HTTP 錯誤: {response.status_code}")
        if not response.text.strip().startswith('{'):
            raise Exception("非 JSON 回應")

        data = response.json()
        df = pd.DataFrame(data['data'], columns=data['fields'])

        df['成交股數'] = df['成交股數'].astype(str).str.replace(',', '').astype(float)
        df = df.sort_values('成交股數', ascending=False)

        selected = df.head(30)
        return [{"symbol": row['證券代號'], "name": row['證券名稱']} for _, row in selected.iterrows()]
    
    except Exception as e:
        print(f"[錯誤] 無法擷取盤前資料: {e}")
        return []
