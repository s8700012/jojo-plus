def generate_features(price):
    # 可擴充技術指標、均線、MACD等，簡化為價格特徵
    return [price, price * 0.95, price * 1.05]
