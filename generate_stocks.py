import yfinance as yf
import json

# 台股常見非權值股代號（可擴充或動態取得）
twse_symbols = [
    "1101", "1216", "1301", "1326", "1402", "2002", "2105", "2207", "2301", "2303",
    "2324", "2354", "2357", "2382", "2395", "2412", "2451", "2454", "2603", "2606",
    "2609", "2615", "2801", "2882", "2891", "3008", "3034", "3037", "3231"
]

all_symbols = [f"{code}.TW" for code in twse_symbols]

def get_top_volume_stocks(limit=30):
    result = []

    for symbol in all_symbols:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1d", interval="1m")
            if df.empty or len(df) < 5:
                continue

            # 抓取 09:00～09:03 成交量
            morning_volume = df.between_time("09:00", "09:03")["Volume"].sum()
            last_price = round(df["Close"].iloc[-1], 2)

            result.append({
                "symbol": symbol.replace(".TW", ""),
                "name": symbol.replace(".TW", ""),  # 可串接 API 查中文名
                "volume": morning_volume,
                "price": last_price
            })
        except Exception as e:
            print(f"[Error] {symbol}: {e}")

    # 依成交量排序取前 N 檔
    sorted_stocks = sorted(result, key=lambda x: x["volume"], reverse=True)[:limit]
    final = [{"symbol": stock["symbol"], "name": stock["name"]} for stock in sorted_stocks]

    with open("stocks.json", "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    print(f"[Info] 已產出 stocks.json（共 {len(final)} 檔）")

if __name__ == "__main__":
    get_top_volume_stocks()
