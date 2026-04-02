from __future__ import annotations
import json
from pathlib import Path

import joblib
import pandas as pd

from .config import MODEL_PATH, METADATA_PATH

def load_artifacts():
    if not MODEL_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError("Model artifacts not found. Run training first.")
    model = joblib.load(MODEL_PATH)
    meta = json.loads(METADATA_PATH.read_text())
    return model, meta

def predict_score(input_df: pd.DataFrame):
    model, meta = load_artifacts()
    feature_cols = meta["feature_columns"]
    X = input_df[feature_cols].copy()
    score = float(model.predict(X)[0])
    if score >= 20:
        category = "Excellent"
    elif score >= 12:
        category = "Good"
    else:
        category = "Needs Improvement"
    return score, category