import json
import random

def generate_dynamic_stocks():
    all_stocks = [
        {"symbol": "2603", "name": "長榮"},
        {"symbol": "2609", "name": "陽明"},
        {"symbol": "2615", "name": "萬海"},
        {"symbol": "1101", "name": "台泥"},
        {"symbol": "1216", "name": "統一"},
        {"symbol": "1301", "name": "台塑"},
        {"symbol": "1326", "name": "台化"},
        {"symbol": "1402", "name": "遠東新"},
        {"symbol": "2002", "name": "中鋼"},
        {"symbol": "2105", "name": "正新"},
        {"symbol": "2207", "name": "和泰車"},
        {"symbol": "2301", "name": "光寶科"},
        {"symbol": "2324", "name": "仁寶"},
        {"symbol": "2354", "name": "鴻準"},
        {"symbol": "2357", "name": "華碩"},
        {"symbol": "2382", "name": "廣達"},
        {"symbol": "2395", "name": "研華"},
        {"symbol": "2412", "name": "中華電"},
        {"symbol": "2451", "name": "創見"},
        {"symbol": "2606", "name": "裕民"},
        {"symbol": "2801", "name": "彰銀"},
        {"symbol": "2882", "name": "國泰金"},
        {"symbol": "3008", "name": "大立光"},
        {"symbol": "3034", "name": "聯詠"},
        {"symbol": "3209", "name": "全科"},
        {"symbol": "4904", "name": "遠傳"},
        {"symbol": "3702", "name": "大聯大"},
        {"symbol": "3037", "name": "欣興"},
        {"symbol": "3231", "name": "緯創"},
        {"symbol": "2345", "name": "智邦"},
        {"symbol": "3706", "name": "神達"},
        {"symbol": "6182", "name": "合晶"},
        {"symbol": "3596", "name": "智易"}
    ]
    
    # 模擬依成交量排序後取前 30 檔
    random.shuffle(all_stocks)
    selected = all_stocks[:30]

    with open("stocks.json", "w", encoding="utf-8") as f:
        json.dump(selected, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generate_dynamic_stocks()
