from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
ARTIFACT_DIR = BASE_DIR / "artifacts"
REPORT_DIR = BASE_DIR / "reports"
FIGURE_DIR = REPORT_DIR / "figures"

RAW_DATA_PATH = DATA_DIR / "virtual_interview_performance_dataset.csv"
TRAINING_DATA_PATH = DATA_DIR / "interview_training_source.csv"
POWERBI_DATA_PATH = DATA_DIR / "interview_powerbi_source.csv"

MODEL_PATH = ARTIFACT_DIR / "best_interview_performance_model.joblib"
METADATA_PATH = ARTIFACT_DIR / "model_metadata.json"
METRICS_PATH = ARTIFACT_DIR / "model_metrics.json"
TARGET_SCORE_COL = "Performance_Score_Proxy"
TARGET_CATEGORY_COL = "Performance_Category"