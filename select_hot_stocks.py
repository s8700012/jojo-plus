import pandas as pd
from datetime import datetime
import json

def load_trade_data(csv_file):
    df = pd.read_csv(csv_file)
    df['time'] = pd.to_datetime(df['time'])
    return df

def filter_non_weighted_stocks(df, weighted_list):
    return df[~df['symbol'].isin(weighted_list)]

def select_top30(df):
    filtered_df = df[(df['time'].dt.time >= datetime.strptime('08:50', '%H:%M').time()) &
                     (df['time'].dt.time <= datetime.strptime('09:00', '%H:%M').time())]
    top = filtered_df.groupby('symbol')['volume'].sum().sort_values(ascending=False).head(30)
    return top.index.tolist()

def save_as_json(symbols, stock_meta_path='all_stocks_meta.json', output_path='stocks.json'):
    with open(stock_meta_path, 'r', encoding='utf-8') as f:
        all_meta = json.load(f)

    selected = [s for s in all_meta if s['symbol'] in symbols]

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(selected, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    df = load_trade_data('preopen_volume.csv')
    weighted = ['2330', '2317', '2454', '2303', '2881']  # 權值股清單
    df = filter_non_weighted_stocks(df, weighted)
    top30 = select_top30(df)
    save_as_json(top30)
