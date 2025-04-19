import requests
import pandas as pd
from datetime import datetime

def get_top30_preopen():
    url = "https://www.twse.com.tw/rwd/zh/preop/preopQ?date={date}&response=json"
    date_str = datetime.now().strftime("%Y%m%d")
    full_url = url.format(date=date_str)

    try:
        response = requests.get(full_url)
        response.encoding = 'utf-8'
        data = response.json()
        df = pd.DataFrame(data['data'], columns=data['fields'])

        df['成交股數'] = df['成交股數'].astype(str).str.replace(',', '').astype(float)
        df = df.sort_values('成交股數', ascending=False)

        selected = df.head(30)
        return [{"symbol": row['證券代號'], "name": row['證券名稱']} for _, row in selected.iterrows()]

    except Exception as e:
        print(f"[錯誤] 無法擷取盤前資料: {e}")
        return []
