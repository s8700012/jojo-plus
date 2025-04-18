import requests
import json
from bs4 import BeautifulSoup

def fetch_preopen_stocks():
    url = "https://www.twse.com.tw/zh/preopen/preopen5"  # 舉例：你需改為真實來源
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 假設網頁中有表格資料
        rows = soup.select("table tbody tr")

        hot_stocks = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 5:
                symbol = cols[0].text.strip()
                name = cols[1].text.strip()
                vol = int(cols[4].text.replace(",", ""))

                # 排除權值股
                if symbol not in ['2330', '2317']:
                    hot_stocks.append({
                        "symbol": symbol,
                        "name": name
                    })

            if len(hot_stocks) >= 30:
                break

        with open("stocks.json", "w", encoding="utf-8") as f:
            json.dump(hot_stocks, f, ensure_ascii=False, indent=2)
        print(f"成功寫入 stocks.json（共 {len(hot_stocks)} 檔）")

    except Exception as e:
        print("擷取失敗：", e)

if __name__ == "__main__":
    fetch_preopen_stocks()
