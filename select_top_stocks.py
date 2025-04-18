import yfinance as yf
import pandas as pd
import json
from datetime import datetime, timedelta

# 排除的權值股
exclude_symbols = ['2330', '2317', '2454', '2881', '2882', '2303']

# 擬定候選台股（實務可改為全市場清單）
candidate_symbols = ['2330', '2317', '2454', '2303', '2881', '2882', '2603', '2609',
                     '2615', '1101', '1216', '1301', '1326', '1402', '2002', '2105',
                     '2207', '2301', '2324', '2354', '2357', '2382', '2395', '2412',
                     '2451', '2606', '2801', '3008', '3034', '3231', '4904', '3702',
                     '3037', '2345']

# 模擬時間範圍（盤前試撮或開盤初期）
start_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
end_time = datetime.now().strftime('%Y-%m-%d')

selected = []
for symbol in candidate_symbols:
    if symbol in exclude_symbols:
        continue
    try:
        ticker = yf.Ticker(f"{symbol}.TW")
        hist = ticker.history(start=start_time, end=end_time, interval="1m")
        volume_sum = hist['Volume'].sum()
        if volume_sum > 0:
            selected.append((symbol, volume_sum))
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# 按成交量排序，取前 30 檔
selected = sorted(selected, key=lambda x: x[1], reverse=True)[:30]

# 加上名稱（實務可改抓 API）
symbol_name_map = {
    '2603': '長榮', '2609': '陽明', '2615': '萬海', '1101': '台泥', '1216': '統一',
    '1301': '台塑', '1326': '台化', '1402': '遠東新', '2002': '中鋼', '2105': '正新',
    '2207': '和泰車', '2301': '光寶科', '2324': '仁寶', '2354': '鴻準', '2357': '華碩',
    '2382': '廣達', '2395': '研華', '2412': '中華電', '2451': '創見', '2606': '裕民',
    '2801': '彰銀', '3008': '大立光', '3034': '聯詠', '3231': '緯創', '4904': '遠傳',
    '3702': '大聯大', '3037': '欣興', '2345': '智邦'
}

result = []
for symbol, _ in selected:
    result.append({"symbol": symbol, "name": symbol_name_map.get(symbol, "")})

# 寫入 stocks.json
with open("stocks.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("stocks.json 已更新")
