def load_model():
    # 模擬載入模型（實際應替換成真實模型）
    return "mock_model"

def predict(model, features):
    # 假設預測方式，未來可替換成 AI 分類器
    if features[0] < features[1]:
        return "做多"
    elif features[0] > features[2]:
        return "做空"
    else:
        return "觀望"
