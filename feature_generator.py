import random

def generate_features(price):
    # 模擬過去幾日價格，實務上應接收歷史資料
    history = [price * (1 + random.uniform(-0.02, 0.02)) for _ in range(10)]
    
    ma5 = sum(history[-5:]) / 5
    ma10 = sum(history[-10:]) / 10
    rsi = calculate_rsi(history)
    macd = ma5 - ma10
    k, d = calculate_kd(history)
    
    return {
        "price": price,
        "ma5": round(ma5, 2),
        "ma10": round(ma10, 2),
        "rsi": round(rsi, 2),
        "macd": round(macd, 2),
        "k": round(k, 2),
        "d": round(d, 2)
    }

def calculate_rsi(history):
    gains = [max(history[i] - history[i - 1], 0) for i in range(1, len(history))]
    losses = [max(history[i - 1] - history[i], 0) for i in range(1, len(history))]
    avg_gain = sum(gains) / len(gains) if gains else 0.01
    avg_loss = sum(losses) / len(losses) if losses else 0.01
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_kd(history):
    high = max(history[-9:])
    low = min(history[-9:])
    close = history[-1]
    rsv = (close - low) / (high - low) * 100 if high != low else 50
    k = 2 / 3 * 50 + 1 / 3 * rsv
    d = 2 / 3 * 50 + 1 / 3 * k
    return k, d
