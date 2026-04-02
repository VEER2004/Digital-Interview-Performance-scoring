from __future__ import annotations
import pandas as pd
from .feature_engineering import build_performance_score, get_model_inputs

def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.drop_duplicates().reset_index(drop=True)
    return out

def prepare_training_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = build_performance_score(df)
    return out

def split_features_target(df: pd.DataFrame):
    y = df["Performance_Score_Proxy"]
    X = get_model_inputs(df)
    return X, y