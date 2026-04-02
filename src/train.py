from __future__ import annotations
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import TRAINING_DATA_PATH, MODEL_PATH, METADATA_PATH, METRICS_PATH, ARTIFACT_DIR
from .preprocess import load_data, clean_data, prepare_training_frame, split_features_target
from .feature_engineering import get_model_inputs

def rmse(y_true, y_pred):
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))

def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric_features = X.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

def evaluate_models(X_train, X_test, y_train, y_test):
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=250, random_state=42, n_jobs=-1, max_depth=16
        ),
        "AdaBoost Regressor": AdaBoostRegressor(
            n_estimators=300, random_state=42, learning_rate=0.05
        ),
        "Gradient Boosting Regressor": GradientBoostingRegressor(
            random_state=42, n_estimators=250, learning_rate=0.05, max_depth=3
        ),
    }

    results = []
    best_name = None
    best_pipeline = None
    best_r2 = -1e9
    for name, model in models.items():
        preprocessor = build_preprocessor(X_train)
        pipe = Pipeline(steps=[("preprocess", preprocessor), ("model", model)])
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        metrics = {
            "model": name,
            "mae": float(mean_absolute_error(y_test, preds)),
            "rmse": rmse(y_test, preds),
            "r2": float(r2_score(y_test, preds)),
        }
        results.append(metrics)
        if metrics["r2"] > best_r2:
            best_r2 = metrics["r2"]
            best_name = name
            best_pipeline = pipe
    return best_name, best_pipeline, results

def main():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data(TRAINING_DATA_PATH)
    df = clean_data(df)
    df = prepare_training_frame(df)
    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    best_name, best_pipeline, results = evaluate_models(X_train, X_test, y_train, y_test)

    preds = best_pipeline.predict(X_test)
    metrics = {
        "best_model": best_name,
        "holdout": {
            "mae": float(mean_absolute_error(y_test, preds)),
            "rmse": rmse(y_test, preds),
            "r2": float(r2_score(y_test, preds)),
        },
        "all_models": results,
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "feature_columns": X.columns.tolist(),
    }

    joblib.dump(best_pipeline, MODEL_PATH)
    METADATA_PATH.write_text(json.dumps({
        "best_model": best_name,
        "feature_columns": X.columns.tolist(),
        "target_name": "Performance_Score_Proxy",
        "category_thresholds": {"Needs Improvement": [0, 12], "Good": [12, 20], "Excellent": [20, 30]},
        "expected_input_schema": {c: str(X[c].dtype) for c in X.columns},
    }, indent=2))

    METRICS_PATH.write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))
    print(f"Saved model to {MODEL_PATH}")

if __name__ == "__main__":
    main()