import yfinance as yf
import datetime
import json

# 權值股列表，可擴充
exclude_symbols = {"2330", "2317", "2454", "2303", "2881", "2891"}

def fetch_dynamic_stocks():
    # 模擬來源，可換成爬蟲擷取實際盤前試撮資料
    stock_pool = ["2603", "2609", "2615", "1101", "1216", "1301", "1326", "1402",
                  "2002", "2105", "2207", "2301", "2324", "2354", "2357", "2382",
                  "2395", "2412", "2451", "2606", "2801", "2882", "3008", "3034",
                  "3209", "4904", "3702", "3037", "3231", "2345", "2330", "2317"]

    results = []
    for symbol in stock_pool:
        if symbol in exclude_symbols:
            continue

        ticker = yf.Ticker(f"{symbol}.TW")
        try:
            history = ticker.history(period="1d", interval="1m")
            recent_volume = history["Volume"][-5:].sum()
            price = round(history["Close"].iloc[-1], 2)
            results.append({
                "symbol": symbol,
                "name": "",  # 可搭配字典查表填入名稱
                "volume": recent_volume,
                "price": price
            })
        except:
            continue

    # 取出成交量最大前 30 檔
    top30 = sorted(results, key=lambda x: x["volume"], reverse=True)[:30]

    # 格式化為 stocks.json 結構
    dynamic_stocks = [{"symbol": s["symbol"], "name": s["symbol"]} for s in top30]
    with open("stocks.json", "w", encoding="utf-8") as f:
        json.dump(dynamic_stocks, f, ensure_ascii=False, indent=2)
    print("stocks.json 已更新")

if __name__ == "__main__":
    fetch_dynamic_stocks()
