# 🎥 Interview Performance Recording System

An **AI-powered interview analysis system** combining real-time video recording with ML predictions.

## 🚀 Quick Start

### Local

```bash
pip install -r requirements.txt
python -m src.train          # If first time
streamlit run app.py
```

### Cloud (Streamlit Cloud)

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide.

**Summary:**

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy!

## ✨ Features

- 🎥 **Continuous video recording** with real-time AI analysis
- 🤖 **Phase 1-4 AI**: Facial, Speech, Body, Unified scoring
- 📊 **Real-time analytics**: Trends, distributions, performance profiles
- 🧠 **ML Predictions**: Linear Regression model (trained)
- 💾 **Data persistence**: Session state keeps all recordings

## 📋 System Architecture

**Video → Phase 1 (Facial) → Phase 2 (Speech) → Phase 3 (Body) → Phase 4 (Unified) → ML Model → Score (0-30)**

**Scoring**: Excellent (≥20) | Good (≥12) | Needs Improvement (<12)

## 📁 Key Files

- `app.py` - Main Streamlit app (cloud-ready)
- `requirements.txt` - Dependencies
- `src/` - ML pipeline and AI modules
- `artifacts/` - Trained model (joblib)
- `DEPLOYMENT.md` - Cloud deployment guide
- `.streamlit/config.toml` - Streamlit settings
