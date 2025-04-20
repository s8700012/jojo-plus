# stock_selector.py
import requests
import pandas as pd
import json

def select_top_30():
    url = 'https://www.twse.com.tw/exchangeReport/TWT48U?response=html'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers, timeout=10)
    res.encoding = 'utf-8'

    # 讀取表格
    dfs = pd.read_html(res.text)
    df = dfs[0]
    df.columns = ['symbol', 'name', '成交股數', '股本', '週轉率']

    df['symbol'] = df['symbol'].astype(str).str.zfill(4)
    df['週轉率'] = pd.to_numeric(df['週轉率'], errors='coerce')
    df = df.dropna(subset=['週轉率'])

    # 排除 ETF、金融股
    df = df[~df['name'].str.contains('富邦|元大|國泰|永豐|中信|群益|兆豐|第一金|台新|統一|凱基|日盛|ETF|基金|債', na=False)]
    df = df[~df['symbol'].str.startswith(('00', '28'))]

    # 取前30
    top30 = df.sort_values('週轉率', ascending=False).head(30)
    selected = top30[['symbol', 'name']].to_dict(orient='records')

    with open('stocks.json', 'w', encoding='utf-8') as f:
        json.dump(selected, f, ensure_ascii=False, indent=2)

    print("[更新成功] 已將前30週轉率熱門股寫入 stocks.json")
