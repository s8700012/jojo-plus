import os
import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np

MODEL_PATH = "model.pkl"

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        return train_model()

def train_model():
    # 假設訓練資料（可改為真實歷史資料）
    X = [[100, 98, 97, 50], [90, 92, 91, 55], [105, 104, 103, 45]]
    y = [1, 0, 1]  # 1=做多, 0=做空
    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model

def predict(model, features):
    x = [[
        features["price"],
        features["ma5"],
        features["ma10"],
        features["rsi"]
    ]]
    y_pred = model.predict(x)[0]
    return "做多" if y_pred == 1 else "做空"

def retrain_with_new_data(new_features, new_label):
    model = load_model()
    x = [[
        new_features["price"],
        new_features["ma5"],
        new_features["ma10"],
        new_features["rsi"]
    ]]
    y = [new_label]
    model.fit(x, y)  # 緊急再訓練
    joblib.dump(model, MODEL_PATH)
