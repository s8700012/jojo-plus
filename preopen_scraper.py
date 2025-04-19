import requests
import pandas as pd
import json
from datetime import datetime

def fetch_preopen_data():
    url = "https://www.twse.com.tw/rwd/zh/preop/preopQ?date={date}&response=json"
    date_str = datetime.now().strftime("%Y%m%d")
    full_url = url.format(date=date_str)
    
    try:
        response = requests.get(full_url)
        response.encoding = 'utf-8'
        data = response.json()
        df = pd.DataFrame(data['data'], columns=data['fields'])

        # 計算週轉率（此處僅以成交股數排序模擬）
        df['成交股數'] = df['成交股數'].astype(str).str.replace(',', '').astype(float)
        df = df.sort_values('成交股數', ascending=False)

        selected = df.head(30)

        result = []
        for _, row in selected.iterrows():
            result.append({
                "symbol": row['證券代號'],
                "name": row['證券名稱']
            })

        with open('stocks.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print("已產生 stocks.json（高週轉率前30檔）")

    except Exception as e:
        print(f"[錯誤] 無法擷取盤前資料: {e}")

if __name__ == "__main__":
    fetch_preopen_data()
