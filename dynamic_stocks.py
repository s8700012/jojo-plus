import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json

# 非權值股清單（可從全市場中排除大型權值股）
EXCLUDE_LIST = ['2330', '2317', '2454', '2303', '2881', '2891']

# 預設候選清單（範例，可改為從全市場爬取）
CANDIDATES = ['2603', '2609', '2615', '1101', '1216', '1301', '1326',
              '1402', '2002', '2105', '2207', '2301', '2324', '2354',
              '2357', '2382', '2395', '2412', '2451', '2606', '2801',
              '2882', '3008', '3034', '3231', '4904', '3702', '3037',
              '3209', '2345']

def fetch_volume(symbol, start_time, end_time):
    try:
        ticker = yf.Ticker(f"{symbol}.TW")
        df = ticker.history(interval="1m", start=start_time, end=end_time)
        return df['Volume'].sum()
    except Exception as e:
        print(f"Error fetching volume for {symbol}: {e}")
        return 0

def select_top30():
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    start_0850 = f"{today} 08:50"
    end_0900 = f"{today} 09:00"
    start_0900 = f"{today} 09:00"
    end_0903 = f"{today} 09:03"

    top_symbols = []

    volume_data = []
    for symbol in CANDIDATES:
        if symbol in EXCLUDE_LIST:
            continue
        vol_preopen = fetch_volume(symbol, start_0850, end_0900)
        vol_open = fetch_volume(symbol, start_0900, end_0903)
        total_vol = vol_preopen + vol_open
        volume_data.append((symbol, total_vol))

    sorted_symbols = sorted(volume_data, key=lambda x: x[1], reverse=True)
    selected = sorted_symbols[:30]

    # 模擬股票名稱對照，可依實際來源擴充
    result = [{"symbol": s[0], "name": f"股票{s[0]}"} for s in selected]

    # 輸出為 stocks.json
    with open("stocks.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result

if __name__ == "__main__":
    selected = select_top30()
    print("已選出熱門 30 檔：")
    for s in selected:
        print(f"{s['symbol']} - {s['name']}")
