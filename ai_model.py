def load_model():
    return "basic_model"

def predict(model, features):
    if not features:
        return "無法預測"

    price = features["price"]
    ma5 = features["ma5"]
    ma10 = features["ma10"]
    rsi = features["rsi"]
    price_change = features["price_change"]

    # 多空邏輯
    if price > ma5 and price > ma10 and rsi > 55 and price_change > 0.003:
        return "做多"
    elif price < ma5 and price < ma10 and rsi < 45 and price_change < -0.003:
        return "做空"
    else:
        return "觀望"
