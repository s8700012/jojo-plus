def load_model():
    return "mock_model_with_kbars"

def predict(model, features):
    """
    使用 1分K、5分K、成交量與大單指標判斷多空：
    - 若現價 > 5MA 且量增，視為多單
    - 若大單淨買超明顯，優先偏多
    """
    score = 0

    # 價格與均線關係
    if features["price"] > features["ma5"]:
        score += 1
    if features["price"] > features["ma10"]:
        score += 1

    # 成交量邏輯
    if features.get("volume") and features["volume"] > features.get("avg_volume", 1):
        score += 1

    # 大單邏輯
    if features.get("big_buy") > features.get("big_sell", 0):
        score += 1

    if score >= 3:
        return "做多"
    elif score <= 1:
        return "做空"
    else:
        return "觀望"
