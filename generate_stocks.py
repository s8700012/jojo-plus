from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

def fetch_hot_stocks(url="https://www.wantgoo.com/stock/hot-trade"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)  # 等待 JS 載入

    stocks = []

    try:
        rows = driver.find_elements(By.CSS_SELECTOR, ".hotStock-table tbody tr")
        for row in rows[:50]:  # 預抓最多前 50 檔
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 3:
                symbol = cols[0].text.strip()
                name = cols[1].text.strip()

                # 過濾權值股
                if symbol not in ["2330", "2317", "2454", "2882", "2881"]:  # 可擴充
                    stocks.append({"symbol": symbol, "name": name})
            if len(stocks) >= 30:
                break
    except Exception as e:
        print(f"[ERROR] 擷取失敗: {e}")
    finally:
        driver.quit()

    return stocks

def save_to_json(stocks, filename="stocks.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print("正在擷取熱門成交量股票...")
    result = fetch_hot_stocks()
    save_to_json(result)
    print("已更新 stocks.json（熱門前 30 檔）")
[
  {"symbol": "2603", "name": "長榮"},
  {"symbol": "2615", "name": "萬海"},
  ...
]
