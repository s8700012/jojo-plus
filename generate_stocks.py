# generate_stocks.py
from preopen_scraper import fetch_preopen_data
import json

def save_to_stocks_json():
    stocks = fetch_preopen_data()
    with open('stocks.json', 'w', encoding='utf-8') as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)
    print("stocks.json 已更新")

if __name__ == '__main__':
    save_to_stocks_json()
