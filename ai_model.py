# AI 模型主程式
def load_model():
    return {"weights": [0.4, 0.3, 0.3]}

def predict(model, features):
    score = sum(w * f for w, f in zip(model['weights'], features))
    return "多" if score > features[0] else "空"
