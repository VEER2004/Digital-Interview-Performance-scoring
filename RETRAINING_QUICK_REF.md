# 🔄 Model Retraining - Quick Reference

## ⚡ 5-Minute Quick Start

### 1️⃣ Prepare Data

```
✅ Create CSV with 27 columns
✅ Add minimum 1,000 rows
✅ Save to: data/interview_training_source_new.csv
```

### 2️⃣ Update Config (if using new file)

Edit `src/config.py`:

```python
TRAINING_DATA_PATH = DATA_DIR / "interview_training_source_new.csv"
```

### 3️⃣ Retrain

```powershell
python -m src.train
```

### 4️⃣ Verify

```
Check: artifacts/model_metrics.json
```

### 5️⃣ Update Apps

- Streamlit: Refresh browser (auto-loads new model)
- Power BI: Rerun predictions with new model

---

## 📊 Required Columns (27)

```
Candidate_ID, Age, Gender, Education_Level,
Position_Applied, Industry, Interview_Round,
Interview_Mode, Duration_Minutes, Camera_On,
Microphone_Clarity, Network_Stability_Score,
Technical_Questions_Answered, Behavioral_Questions_Answered,
Coding_Test_Score, Eye_Contact_Score, Body_Language_Score,
Speech_Speed_WPM, Filler_Words_Used, Confidence_Score,
Response_Relevance_Score, Interviewer_Rating,
Background_Noise_Level, Follow_Up_Questions_Asked,
Dressing_Appropriateness, Time_Management_Score,
Performance_Score_Proxy
```

---

## ⚙️ What Gets Updated

| File                                      | Updated? | Purpose              |
| ----------------------------------------- | -------- | -------------------- |
| `best_interview_performance_model.joblib` | ✅ YES   | New trained model    |
| `model_metrics.json`                      | ✅ YES   | New R², MAE, RMSE    |
| `model_metadata.json`                     | ✅ YES   | Feature info         |
| `permutation_importance.csv`              | ✅ YES   | Feature ranking      |
| `app.py`                                  | ❌ NO    | Auto-loads new model |
| Training script                           | ❌ NO    | Reused as-is         |

---

## 🚀 Automation Scripts

### Run Monthly Retraining

```powershell
# Save as: retrain_monthly.ps1
$date = Get-Date -Format "yyyy-MM-dd"
Write-Host "Starting retraining: $date"
python -m src.train
Write-Host "Complete at: $(Get-Date)"
```

### Compare Model Versions

```powershell
# Save as: compare_models.ps1
python retrain_model.py
# Shows R², MAE, RMSE comparison
```

---

## 📈 Performance Tracking

### Current Model

```
R² Score: 0.9924 ✅
MAE: 0.2244
RMSE: 0.2755
```

### After Retraining

- Track improvements in model_retraining_log.json
- Compare against baseline
- A/B test if improvement <1%

---

## ⚠️ Common Issues

| Problem         | Solution                                           |
| --------------- | -------------------------------------------------- |
| Missing columns | Verify 27 columns present with exact names         |
| Null values     | Fill with appropriate defaults or remove rows      |
| Wrong data type | Convert strings to proper format (Yes/No, not 1/0) |
| Model worse     | Check data quality; might need more records        |
| Training slow   | Reduce dataset or close other apps                 |

---

## 🎯 When to Retrain

| Scenario                | Frequency              |
| ----------------------- | ---------------------- |
| New batch of interviews | After 500+ new records |
| Continuous updates      | Monthly                |
| Performance degradation | On-demand              |
| Seasonal changes        | Quarterly              |
| Major process changes   | Immediate              |

---

## 📁 File Locations

```
Input:
  data/interview_training_source_new.csv

Output:
  artifacts/best_interview_performance_model.joblib
  artifacts/model_metrics.json
  model_retraining_log.json

Guides:
  MODEL_RETRAINING_GUIDE.md (Detailed)
  SAMPLE_DATA_TEMPLATE.md (Data format)
  retrain_model.py (Example script)
```

---

## 🔗 Quick Links

📖 Full Guide: [MODEL_RETRAINING_GUIDE.md](MODEL_RETRAINING_GUIDE.md)
📋 Data Format: [SAMPLE_DATA_TEMPLATE.md](SAMPLE_DATA_TEMPLATE.md)
📊 Example Script: [retrain_model.py](retrain_model.py)

---

## ✅ Checklist Before Retraining

- [ ] Data prepared (27 columns, 1000+ rows)
- [ ] CSV saved in `data/` folder
- [ ] Config updated (if new file)
- [ ] Backup created (optional but recommended)
- [ ] System has 4GB+ RAM free
- [ ] No other apps consuming resources

---

## 🚀 Ready?

```powershell
# Execute:
python -m src.train

# Monitor:
Get-Content artifacts/model_metrics.json | ConvertFrom-Json
```

---

**Happy Retraining! 🎉**
