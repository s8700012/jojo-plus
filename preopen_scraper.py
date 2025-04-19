import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_market_data():
    url = "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX20?date=&response=json&_=1680400000000"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        json_data = res.json()

        if "tables" not in json_data or len(json_data["tables"]) == 0:
            raise Exception("無法擷取表格資料")

        rows = json_data["tables"][0]["data"]
        df = pd.DataFrame(rows, columns=json_data["tables"][0]["fields"])
        df = df[["證券代號", "證券名稱", "成交股數", "成交金額", "收盤價", "成交筆數"]]

        df["成交股數"] = df["成交股數"].astype(str).str.replace(",", "").astype(float)
        df["成交金額"] = df["成交金額"].astype(str).str.replace(",", "").astype(float)
        df["成交筆數"] = df["成交筆數"].astype(str).str.replace(",", "").astype(float)
        df["收盤價"] = df["收盤價"].astype(str).str.replace(",", "").astype(float)

        df["週轉率%"] = round((df["成交股數"] / 1000) / 1000000 * 100, 2)  # 模擬週轉率公式

        df = df.sort_values("成交金額", ascending=False)
        top30 = df.head(30)

        results = []
        for _, row in top30.iterrows():
            results.append({
                "symbol": row["證券代號"],
                "name": row["證券名稱"],
                "price": round(row["收盤價"], 2),
                "volume": int(row["成交股數"]),
                "turnover_rate": row["週轉率%"]
            })
        return results

    except Exception as e:
        print(f"[錯誤] 擷取資料失敗: {e}")
        return []

# 每次執行測試用
if __name__ == "__main__":
    stocks = fetch_market_data()
    for stock in stocks:
        print(f"{stock['symbol']} {stock['name']} 價格: {stock['price']} 週轉率: {stock['turnover_rate']}%")
        time.sleep(0.1)  # 減少輸出速度以測試
