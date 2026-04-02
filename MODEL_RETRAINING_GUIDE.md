# 🔄 Model Retraining Guide

## How to Retrain Your Model with New Data

Your current model (99.2% accuracy) can be improved or updated with new interview data. Here's how:

---

## 📊 **Data Requirements**

### Required Columns (25 features + target)

Your new training data must have these columns:

```
Candidate_ID, Age, Gender, Education_Level, Position_Applied,
Industry, Interview_Round, Interview_Mode, Duration_Minutes,
Camera_On, Microphone_Clarity, Network_Stability_Score,
Technical_Questions_Answered, Behavioral_Questions_Answered,
Coding_Test_Score, Eye_Contact_Score, Body_Language_Score,
Speech_Speed_WPM, Filler_Words_Used, Confidence_Score,
Response_Relevance_Score, Interviewer_Rating, Background_Noise_Level,
Follow_Up_Questions_Asked, Dressing_Appropriateness, Time_Management_Score,
Performance_Score_Proxy
```

### Data Format

- **File Type**: CSV (Comma-separated values)
- **Location**: Place in `data/` folder
- **Minimum Rows**: 1,000+ records recommended
- **No Missing Values**: Fill all cells

### Example Data Row

```
C9999,32,Female,Masters,Software Engineer,Tech,HR,Zoom,45,Yes,Good,8.5,
8,4,95,7,8,120,2,8,9,4.2,Low,3,Business Casual,8,18.5
```

---

## 🚀 **Step 1: Prepare Your Data**

### Option A: Update Existing File

Replace the current training data:

```
data/interview_training_source.csv
```

### Option B: Use New File

Create a new file:

```
data/interview_training_source_v2.csv
```

### Data Quality Checklist

- [ ] All 27 columns present
- [ ] No empty cells
- [ ] Performance_Score_Proxy ranges 0-20
- [ ] Confidence_Score ranges 1-10
- [ ] Interviewer_Rating ranges 1-5
- [ ] Yes/No values are consistent
- [ ] Min 1,000 rows

---

## 🔧 **Step 2: Update Config (if using new file)**

Edit `src/config.py`:

```python
# Current (if updating existing)
TRAINING_DATA_PATH = DATA_DIR / "interview_training_source.csv"

# Or new file
TRAINING_DATA_PATH = DATA_DIR / "interview_training_source_v2.csv"
```

---

## 🎯 **Step 3: Retrain the Model**

### In PowerShell:

```powershell
# From project root
python -m src.train
```

### What Happens:

1. **Loads** new training data
2. **Preprocesses** (handles missing values, scaling)
3. **Trains 4 models**:
   - Linear Regression
   - Random Forest Regressor
   - AdaBoost Regressor
   - Gradient Boosting Regressor
4. **Evaluates** all models
5. **Selects** best performer
6. **Saves** new model to `artifacts/best_interview_performance_model.joblib`
7. **Generates** metrics report

### Expected Output:

```
{
  "best_model": "Linear Regression",
  "holdout": {
    "mae": 0.224,
    "rmse": 0.276,
    "r2": 0.9924
  },
  "all_models": [...]
}
```

---

## 📈 **Step 4: Verify Performance**

### Check Metrics

```
artifacts/model_metrics.json
```

### Key Metrics to Monitor

| Metric   | Good Range | Current   |
| -------- | ---------- | --------- |
| R² Score | >0.90      | 0.9924 ✅ |
| MAE      | <0.5       | 0.224 ✅  |
| RMSE     | <0.5       | 0.276 ✅  |

### If Performance Decreased:

- Check data quality
- Verify all 25 features present
- Ensure no data corruption
- Try with more data (>2,000 rows)

---

## 🔄 **Step 5: Update Your Apps**

### Streamlit App (Auto-updates)

- Automatically loads new model on reload
- Just refresh http://localhost:8501
- No code changes needed

### Power BI (Manual)

- Retrain predictions by rerunning your Power BI queries
- Or export new predictions to CSV

---

## 💡 **Common Scenarios**

### Scenario 1: Adding 500 New Records

```powershell
# Combine with existing
cat data/interview_training_source.csv data/new_records.csv > data/combined.csv

# Update config.py
TRAINING_DATA_PATH = DATA_DIR / "combined.csv"

# Retrain
python -m src.train
```

### Scenario 2: Monthly Retraining

```powershell
# Create schedule to run monthly
# Run: python -m src.train

# Script for automated retraining (save as retrain.ps1)
$date = Get-Date -Format "yyyy-MM-dd"
Write-Host "Starting retraining at $date"
python -m src.train
Write-Host "Retraining complete"
```

### Scenario 3: A/B Testing Models

```powershell
# Save old model first
Copy-Item artifacts/best_interview_performance_model.joblib `
  artifacts/best_interview_performance_model_v1.joblib

# Retrain
python -m src.train

# Compare metrics between v1 and new model
```

---

## 🔍 **What Changes During Retraining**

### Updates:

- ✅ Model weights/coefficients
- ✅ Performance metrics
- ✅ Feature importance
- ✅ Prediction accuracy

### Stays the Same:

- ✅ Feature engineering logic
- ✅ Preprocessing pipeline
- ✅ Streamlit app interface
- ✅ Model architecture

---

## ⚠️ **Troubleshooting**

### Issue: "ModuleNotFoundError"

```powershell
# Reinstall dependencies
.\venv\Scripts\pip install -r requirements.txt
```

### Issue: Model Performance Worse

- Verify new data quality
- Check if new data has different distribution
- Ensure all 25 features present
- Try with more records (minimum 1,000)

### Issue: Training Takes Too Long

- Reduce dataset (split into batches)
- Check system resources (RAM, CPU)
- Use fewer trees in Random Forest (reduce n_estimators)

---

## 📊 **Monitoring Model Performance Over Time**

### Create a Log File

```python
# Add to src/train.py after training
import json
from datetime import datetime

log_entry = {
    "date": datetime.now().isoformat(),
    "r2": metrics["holdout"]["r2"],
    "mae": metrics["holdout"]["mae"],
    "rmse": metrics["holdout"]["rmse"],
    "best_model": metrics["best_model"],
    "train_rows": train_rows,
    "test_rows": test_rows
}

# Append to log
with open("model_training_log.json", "a") as f:
    f.write(json.dumps(log_entry) + "\n")
```

### Track Improvements

```
Date       | R² Score | MAE   | RMSE  | Model
-----------|----------|-------|-------|------------------
2026-04-02 | 0.9924   | 0.224 | 0.276 | Linear Regression
2026-05-02 | 0.9938   | 0.198 | 0.245 | Linear Regression
2026-06-02 | 0.9951   | 0.187 | 0.231 | Gradient Boosting
```

---

## 🎯 **Best Practices for Retraining**

### 1. **Version Control Your Data**

```
data/interview_training_source_v1.csv
data/interview_training_source_v2.csv
data/interview_training_source_latest.csv
```

### 2. **Keep Backup Models**

```
artifacts/best_interview_performance_model_v1.joblib
artifacts/best_interview_performance_model_v2.joblib
artifacts/best_interview_performance_model_backup.joblib
```

### 3. **Document Changes**

```
model_changelog.md
- v1: Initial model (2000 records, R²=0.9924)
- v2: Added 500 new records (2500 total, R²=0.9938)
- v3: Seasonal data (3000 total, R²=0.9951)
```

### 4. **Retrain Schedule**

- **Weekly**: If adding 100+ records/week
- **Monthly**: Standard update cycle
- **Quarterly**: Major retraining with full dataset
- **On-demand**: When performance degrades

### 5. **Validation Process**

- Always train/test split
- Monitor metrics over time
- Compare against baseline model
- A/B test before deployment

---

## 📁 **Files Modified During Retraining**

```
✅ artifacts/best_interview_performance_model.joblib (Updated)
✅ artifacts/model_metrics.json (Updated)
✅ artifacts/model_metadata.json (Updated)
✅ artifacts/permutation_importance.csv (Updated)

📝 No changes to:
   - src/train.py
   - src/preprocess.py
   - src/feature_engineering.py
   - app.py
```

---

## 🚀 **Ready to Retrain?**

### Quick Checklist:

- [ ] New data prepared in CSV format
- [ ] 27 required columns present
- [ ] Minimum 1,000 rows
- [ ] No missing values
- [ ] File placed in `data/` folder
- [ ] Config updated (if using new file)

### Execute:

```powershell
python -m src.train
```

### Verify:

```
Check artifacts/model_metrics.json for new R² score
```

---

## 📞 **Next Steps**

1. **Prepare your new data** (follow requirements above)
2. **Run retraining** (`python -m src.train`)
3. **Check metrics** (compare to baseline)
4. **Update apps** if needed
5. **Monitor performance** over time

Your model will automatically improve with more diverse, high-quality data!

---

**Happy Retraining! 🚀**
