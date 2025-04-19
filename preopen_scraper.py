# preopen_scraper.py
import requests
import pandas as pd
import json
from datetime import datetime

def fetch_market_data(top_n=30):
    url = "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX20?date=&response=json"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }

    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 擷取資料中...")
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        json_data = res.json()

        if "tables" not in json_data or len(json_data["tables"]) == 0:
            raise Exception("找不到有效資料表格")

        table = json_data["tables"][0]
        rows = table["data"]
        columns = table["fields"]

        df = pd.DataFrame(rows, columns=columns)
        df = df[["證券代號", "證券名稱", "成交股數", "成交金額", "收盤價", "成交筆數"]].copy()
        for col in ["成交股數", "成交金額", "成交筆數", "收盤價"]:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors='coerce').fillna(0)

        df["週轉率%"] = round(df["成交股數"] / 1000000 * 100, 2)
        df = df.sort_values("成交金額", ascending=False)
        top_stocks = df.head(top_n)

        results = []
        for _, row in top_stocks.iterrows():
            results.append({
                "symbol": row["證券代號"],
                "name": row["證券名稱"]
            })

        # 儲存至 stocks.json（需使用絕對路徑）
        with open("stocks.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"[成功] 已更新 stocks.json，共 {len(results)} 檔")
        return results

    except Exception as e:
        print(f"[錯誤] 擷取失敗: {e}")
        return []

# 測試用
if __name__ == "__main__":
    fetch_market_data()
