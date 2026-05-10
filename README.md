# 🎯 Digital Interview Performance Scoring System

> An AI-powered, end-to-end digital interview evaluation platform that combines supervised machine learning, computer vision, NLP, and live proctoring to produce standardized, bias-free candidate performance scores.

---

## 📋 Abstract

This project uses machine learning to evaluate candidate performance in digital interviews by analyzing facial expressions, tone, body language, and speech quality. Computer vision models extract visual cues such as eye contact, confidence level, and engagement. NLP techniques assess verbal clarity, sentiment, and communication effectiveness. The system produces a performance score that helps HR teams make data-driven hiring decisions. This approach enhances fairness, reduces manual bias, and supports scalable remote recruitment.

---

## 📌 Table of Contents

1. [Problem Definition & Objective](#1-problem-definition--objective)
2. [Project Architecture](#2-project-architecture)
3. [Dataset](#3-dataset)
4. [Data Preprocessing](#4-data-preprocessing)
5. [Exploratory Data Analysis (EDA)](#5-exploratory-data-analysis-eda)
6. [Machine Learning Pipeline](#6-machine-learning-pipeline)
7. [Application Features (Tab-by-Tab)](#7-application-features-tab-by-tab)
8. [Advanced Analytics Module](#8-advanced-analytics-module)
9. [Live Proctoring System](#9-live-proctoring-system)
10. [AI Video Scorer (Automated Analysis)](#10-ai-video-scorer-automated-analysis)
11. [UI/UX Design System](#11-uiux-design-system)
12. [Tech Stack & Dependencies](#12-tech-stack--dependencies)
13. [Project File Structure](#13-project-file-structure)
14. [Setup & Installation Guide](#14-setup--installation-guide)
15. [How to Run](#15-how-to-run)
16. [Output & Scoring Logic](#16-output--scoring-logic)
17. [Performance Metrics](#17-performance-metrics)
18. [Future Improvements](#18-future-improvements)

---

## 1. Problem Definition & Objective

### Objective
To develop an AI-based system that predicts and scores candidate interview performance using structured interview metrics combined with real-time behavioral and speech analysis.

### Problem Type
- **Domain:** Human Resources / Recruitment Technology
- **ML Category:** Supervised Machine Learning
- **Task Type:** Regression Problem (predicting a continuous performance score)

### Business Need
Traditional interview processes are:
- Prone to **human bias** (unconscious favoritism, cultural bias)
- **Inconsistent** across different interviewers and rounds
- **Non-scalable** for high-volume recruitment
- **Slow** — requiring manual review and consensus

This system addresses all of the above by:
- Standardizing the evaluation framework through a consistent metric set
- Using AI to extract behavioral signals (facial expressions, voice tone, eye contact)
- Producing an objective, reproducible performance score
- Supporting both live interviews (via proctoring) and asynchronous video review

---

## 2. Project Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Web App (app.py)             │
│                                                         │
│  ┌───────────┐ ┌───────────┐ ┌────────────────────────┐ │
│  │ Manual    │ │ Advanced  │ │  Live Proctoring +      │ │
│  │ Input     │ │ Analytics │ │  AI Video Upload Scorer │ │
│  │ (Tabs 1-4)│ │ (Tab 5)   │ │  (Tabs 6 & 7)          │ │
│  └─────┬─────┘ └─────┬─────┘ └────────────┬───────────┘ │
│        │              │                    │              │
│        ▼              ▼                    ▼              │
│  ┌─────────────────────────────────────────────────────┐ │
│  │         Feature Aggregation Layer                   │ │
│  │  (Structured Metrics + CV Scores + NLP Scores)      │ │
│  └─────────────────────┬───────────────────────────────┘ │
│                        ▼                                 │
│  ┌─────────────────────────────────────────────────────┐ │
│  │         ML Inference Engine                         │ │
│  │   best_interview_performance_model.pkl (Ensemble)   │ │
│  │   scaler.pkl (StandardScaler)                       │ │
│  └─────────────────────┬───────────────────────────────┘ │
│                        ▼                                 │
│  ┌─────────────────────────────────────────────────────┐ │
│  │     Power BI-Style Plotly Dashboard + Suggestions   │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Offline Components
| Script | Purpose |
|--------|---------|
| `data_generator.py` | Generates synthetic training data if Kaggle dataset is unavailable |
| `train_model.py` | Trains multiple models, selects the best, saves `.pkl` artifacts |
| `eda.py` | Runs automated Exploratory Data Analysis and saves plots to `eda_plots/` |

### Online Components (Streamlit App)
| File | Purpose |
|------|---------|
| `app.py` | Full Streamlit UI with 7 tabs, proctoring, NLP, CV, and ML inference |

---

## 3. Dataset

### Dataset Used
**Virtual Interview Performance Dataset**  
Source: [Kaggle — maham9/virtual-interview-performance-dataset](https://www.kaggle.com/datasets/maham9/virtual-interview-performance-dataset)  
File: `virtual_interview_with_target.csv`

### Features
| Feature | Type | Description |
|---------|------|-------------|
| Age | Numeric | Candidate's age |
| Education Score | Float (1-10) | Level of education relative to role requirements |
| Technical Questions Answered | Integer (0-10) | Number of technical questions correctly answered |
| Coding Test Score | Float (0-100) | Score on the automated coding assessment |
| Behavioural Questions Answered | Integer (0-10) | Number of behavioral questions answered effectively |
| Eye Contact Score | Float (1-10) | Estimated eye contact maintained during the interview |
| Confidence Score | Float (1-10) | Observed confidence and composure |
| Speech Speed (WPM) | Integer | Words per minute spoken during the interview |
| Filler Words Used | Integer | Count of "um", "uh", "like" etc. used |
| Interviewer Rating | Float (1-10) | Rating given by the human interviewer |
| Time Management Score | Float (1-10) | Ability to answer within given time limits |
| Round Score | Float (1-10) | Score for the specific interview round |
| Duration | Integer (mins) | Total interview duration |
| Network Stability | Float (1-10) | Quality of video connection during interview |

### Target Variable
`Final Interview Performance Score` — A continuous numerical score representing overall candidate performance.

---

## 4. Data Preprocessing

The following preprocessing steps are applied inside `train_model.py`:

1. **Load Dataset** — reads `virtual_interview_with_target.csv` using pandas
2. **Drop Duplicates** — removes duplicate rows to prevent model overfitting
3. **Handle Missing Values** — drops any rows with null/NaN values
4. **Feature Selection** — selects only the 14 structured metrics listed above as features (X)
5. **Target Separation** — extracts `Final Interview Performance Score` as the target (y)
6. **Train/Test Split** — splits 80% for training, 20% for testing using `train_test_split`
7. **Standard Scaling** — applies `StandardScaler` to normalize features to zero mean and unit variance, preventing any single feature from dominating the model
8. **Save Scaler** — the fitted scaler is persisted to `scaler.pkl` so the app uses the same normalization at inference time

---

## 5. Exploratory Data Analysis (EDA)

Run `python eda.py` to automatically generate and save the following visualizations to the `eda_plots/` directory:

| Plot File | Description |
|-----------|-------------|
| `correlation_heatmap.png` | Heatmap of feature-to-feature and feature-to-target correlations |
| `feature_importance.png` | Bar chart of feature importance from a Random Forest regressor |
| `distribution_final_score.png` | Histogram of the target variable distribution |
| `coding_vs_final.png` | Scatter plot of Coding Test Score vs. Final Performance Score |
| `filler_vs_confidence.png` | Scatter plot showing the inverse relationship between filler words and confidence |

These plots are used to validate data quality, understand relationships between features, and justify the feature set chosen for the final model.

---

## 6. Machine Learning Pipeline

### Training Script (`train_model.py`)

The training pipeline evaluates the following algorithms and dynamically selects the best performer based on R² score on the test set:

| Algorithm | Library | Notes |
|-----------|---------|-------|
| Linear Regression | scikit-learn | Baseline model |
| Random Forest Regressor | scikit-learn | Non-linear, handles feature interactions |
| AdaBoost Regressor | scikit-learn | Boosting approach, reduces bias |
| Gradient Boosting Regressor | scikit-learn | Sequentially improves weak learners |
| **Voting Regressor (Ensemble)** | scikit-learn | Combines all 4 models via averaging |

### Model Selection Logic
```python
# Evaluate all models and their R2 scores
# If Ensemble R2 >= best individual model R2 → use Ensemble
# Otherwise → use best individual model
```

### Saved Artifacts
After training, three files are persisted for use by the web app:

| File | Purpose |
|------|---------|
| `best_interview_performance_model.pkl` | The trained regression model (or ensemble) |
| `scaler.pkl` | The fitted StandardScaler for feature normalization |
| `feature_columns.pkl` | The exact list of feature column names (ensures correct ordering at inference) |

### Performance Evaluation
The model is evaluated using:
- **R² Score (Coefficient of Determination)** — measures how much variance in the target the model explains
- **Mean Absolute Error (MAE)** — average absolute prediction error
- **Root Mean Squared Error (RMSE)** — penalizes large errors more

---

## 7. Application Features (Tab-by-Tab)

The Streamlit web app (`app.py`) is organized into **7 interactive tabs**:

---

### Tab 1 — Candidate Info
Collects basic candidate background information:
- **Age** — integer between 18 and 65
- **Education Score (1–10)** — formatted as a clean digital number input

Layout: 2-column grid

---

### Tab 2 — Interview Logistics
Collects metadata about the interview session:
- **Interview Duration (mins)** — total time of the interview
- **Network Stability (1–10)** — quality of the video connection
- **Round Score (1–10)** — score for the specific interview round

Layout: 3-column grid

---

### Tab 3 — Technical & Behavioral
Evaluates the candidate's technical and problem-solving performance:
- **Technical Questions Answered (0–10)** — count of correct technical responses
- **Coding Test Score (0–100)** — result from coding assessment
- **Behavioural Questions Answered (0–10)** — count of behavioral answers

Layout: 3-column grid

---

### Tab 4 — Soft Skills
Evaluates the candidate's interpersonal and communication qualities:
- **Eye Contact Score (1–10)**
- **Confidence Score (1–10)**
- **Speech Speed (WPM)**
- **Filler Words Used**
- **Time Management Score (1–10)**
- **Interviewer Rating (1–10)**

Layout: 3-column grid (2 inputs per column)

> All inputs in Tabs 1–4 are precise **digital number inputs** (not sliders) allowing the interviewer to type exact values.

---

## 8. Advanced Analytics Module

### Tab 5 — Advanced Analytics

This tab implements three real-time AI analysis modules:

#### 8.1 NLP Sentiment Analysis
- The interviewer (or system) pastes the candidate's interview transcript into a text area
- **TextBlob** computes the sentiment polarity score (range: -1.0 to +1.0)
  - Positive score → confident, optimistic communication
  - Negative score → defensive, uncertain communication
- The sentiment score is displayed and can inform the Interviewer Rating input

#### 8.2 Facial Emotion Detection (OpenCV)
- The interviewer takes a snapshot using the built-in webcam input
- **OpenCV** loads `haarcascade_frontalface_default.xml` and `haarcascade_smile.xml`
- The system detects:
  - Whether a face is present in the frame
  - Whether the candidate is smiling (positive emotion indicator)
- A bounding box is drawn on the detected face
- An **Emotion Score (%)** is calculated:
  - Smile detected → 85% (Positive Emotion)
  - No smile → 50% (Neutral)
  - No face → Warning displayed

#### 8.3 Voice Tone Stability Analysis
- The interviewer uploads a `.wav` audio clip of the candidate's response
- **SciPy** reads the audio waveform data
- The standard deviation of the audio signal is calculated as a proxy for voice stability
  - Low std → calm, steady delivery
  - High std → erratic, nervous speech pattern
- A **Voice Tone Stability Score (1–10)** is computed and displayed

---

## 9. Live Proctoring System

### Tab 6 — Live Proctoring

This is the real-time monitoring module designed to simulate a proctored interview environment. It uses `streamlit-webrtc` for live WebRTC streaming.

#### 9.1 Face Tracking (Video Frame Callback)
A real-time video processor runs on every incoming frame from the webcam:
- **One face detected → Green bounding box** with "CANDIDATE DETECTED" label
- **No face detected → Red warning text**: "WARNING: NO FACE DETECTED"
- **Multiple faces detected → Red warning text**: "WARNING: MULTIPLE PEOPLE DETECTED"

#### 9.2 Live Audio Capture & Tone Analysis
An `AudioProcessor` class accumulates live audio frames from the microphone:
- Each audio frame's data is stored in a thread-safe buffer
- The standard deviation of the audio signal is computed per-frame (voice tone stability)

#### 9.3 Live Speech Transcription
- Audio frames are buffered in the `AudioProcessor`
- The interviewer can click **"Transcribe Current Audio Buffer"** at any time
- The system:
  1. Concatenates all buffered audio frames into a single WAV array
  2. Writes it to a temporary `.wav` file
  3. Passes it to **Google Speech Recognition** (`SpeechRecognition` library)
  4. Appends the recognized text to the **Live Transcript** text area
- The transcript grows incrementally as the interview progresses

#### 9.4 Tab Switch / Cheating Detection
- A JavaScript `visibilitychange` event listener is injected into the browser DOM via `components.html`
- If the candidate switches to another browser tab or minimizes the window, a native browser **alert popup** immediately fires:
  > "PROCTORING ALERT: You have switched tabs or minimized the window. This incident has been recorded."

#### 9.5 Screen Sharing Observation
- A JavaScript block using `navigator.mediaDevices.getDisplayMedia()` is rendered
- A **"Start Screen Share"** button asks the candidate's browser to share their screen
- The candidate's screen is streamed live inside the proctoring panel with a red warning border
- The button auto-hides once sharing begins

---

## 10. AI Video Scorer (Automated Analysis)

### Tab 7 — 🎬 AI Video Scorer

This module allows an interviewer to **upload a recorded interview video** (MP4, AVI, or MOV) for fully automated AI scoring — no live session required.

#### Processing Pipeline

**Step 1 — Audio Extraction & Transcription**
- `moviepy (VideoFileClip)` extracts the audio track from the uploaded video
- Audio is saved as a temporary `.wav` file
- `SpeechRecognition` + Google STT converts the speech to text automatically
- A **Voice Tone Stability Score (1–10)** is computed from the audio waveform standard deviation

**Step 2 — Frame-by-Frame Face & Emotion Analysis**
- `OpenCV VideoCapture` reads the video file frame by frame
- Every 15th frame is analyzed (for performance efficiency) using Haar Cascade classifiers:
  - `haarcascade_frontalface_default.xml` → detects face presence
  - `haarcascade_smile.xml` → detects smiling (confidence indicator)
- Counters track:
  - `face_frames` — frames where the face is detected
  - `smile_frames` — frames where a smile is detected
  - `no_face_frames` — frames where no face is present

**Step 3 — NLP Sentiment Analysis**
- `TextBlob` analyzes the transcribed text for sentiment polarity
- The raw polarity (-1 to 1) is mapped to an NLP Score (1 to 10)

**Step 4 — Scoring & Dashboard Generation**
Computed scores:
| Metric | Calculation |
|--------|-------------|
| Eye Contact Score | `face_frames / total_analyzed × 10` |
| Confidence Score | `smile_frames / total_analyzed × 10` |
| Voice Tone Stability | `normalized std_dev of audio waveform` |
| NLP Sentiment Score | `(sentiment_polarity + 1) / 2 × 10` |
| **Overall AI Score** | `mean(all 4 scores)` |

**Step 5 — Plotly Dashboard**
- **Gauge Chart** — displays the Overall AI Score (0–10) with color zones (red/blue/green)
- **Radar Chart** — spider-web visualization of all 4 individual metric scores
- **Metric Cards** — displays each sub-score clearly with icons

**Step 6 — Verdict & Suggestions**
Smart conditional suggestions are generated based on thresholds:
- Eye Contact < 5 → "Candidate was frequently off-camera"
- Confidence Score < 4 → "Low positive expression — recommend mock interviews"
- Voice Tone < 5 → "High tone variation — recommend speech coaching"
- NLP Score < 5 → "Negative/neutral communication — encourage positive framing"
- Face absent > 50% of frames → "⚠️ PRESENCE ALERT"

Final verdict:
- Score ≥ 7 → **🌟 Excellent Candidate** — Fast-track recommended
- Score ≥ 5 → **👍 Good Candidate** — Consider with improvements
- Score < 5 → **⚠️ Needs Significant Improvement** — Not recommended

---

## 11. UI/UX Design System

### Theme
- **Background:** Deep space radial gradient (`#1e1b4b` → `#020617`)
- **Font:** Google Fonts — `Outfit` (weights: 300, 400, 600, 800)
- **Text Color:** `#e2e8f0` (cool gray-white)
- **Heading Color:** `#f8fafc` (pure white), bold, tight letter-spacing

### Components

| Element | Style |
|---------|-------|
| Input Fields | Semi-transparent glass effect, rounded corners, purple glow on focus |
| Primary Button | Pink-to-indigo gradient, scale + shadow animation on hover |
| Tabs | Pill-style, subtle background highlight on active tab |
| Metric Cards | Large bold value in `#10b981` (emerald green) |
| Charts | Fully transparent background to blend with dark theme |
| Alerts | Standard Streamlit warning/error/success/info colors |

### Interactivity
- All hover effects use smooth CSS `transition: all 0.3s cubic-bezier(...)` easing
- Buttons scale up (`scale(1.02)`) and lift (`translateY(-3px)`) on hover with a pink shadow bloom
- Input fields illuminate with a purple `box-shadow` ring on focus

---

## 12. Tech Stack & Dependencies

### Core
| Library | Version | Use |
|---------|---------|-----|
| Python | 3.10+ | Runtime |
| pandas | latest | Data handling & preprocessing |
| numpy | latest | Numerical operations |
| scikit-learn | latest | ML models, scaling, evaluation |
| joblib | latest | Saving/loading model artifacts |
| streamlit | latest | Web application framework |

### Visualization
| Library | Use |
|---------|-----|
| matplotlib | Static EDA plots |
| seaborn | Enhanced statistical visualizations |
| plotly | Interactive Gauge and Radar charts |

### Advanced AI
| Library | Use |
|---------|-----|
| textblob | NLP sentiment analysis |
| opencv-python | Facial emotion detection (Haar Cascades) |
| scipy | Audio waveform analysis (tone stability) |
| SpeechRecognition | Speech-to-text transcription |
| pyaudio | Microphone audio backend |
| moviepy | Video-to-audio extraction for AI Video Scorer |

### Proctoring
| Library | Use |
|---------|-----|
| streamlit-webrtc | Real-time webcam + mic WebRTC stream |
| av | Audio/Video frame processing |
| tornado | ASGI server (WebRTC dependency) |

---

## 13. Project File Structure

```
BrainyBEAM Final/
│
├── app.py                              # Main Streamlit application (7 tabs)
├── train_model.py                      # ML training pipeline + ensemble selection
├── data_generator.py                   # Synthetic dataset generator
├── eda.py                              # Automated EDA plots generator
├── requirements.txt                    # All Python dependencies
├── README.md                           # This documentation
│
├── virtual_interview_with_target.csv   # Kaggle dataset (place here before training)
│
├── best_interview_performance_model.pkl  # Trained ML model (generated by train_model.py)
├── scaler.pkl                          # Fitted StandardScaler (generated by train_model.py)
├── feature_columns.pkl                 # Feature column names (generated by train_model.py)
│
└── eda_plots/                          # Auto-generated EDA visualizations
    ├── correlation_heatmap.png
    ├── feature_importance.png
    ├── distribution_final_score.png
    ├── coding_vs_final.png
    └── filler_vs_confidence.png
```

---

## 14. Setup & Installation Guide

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Internet connection (for Google Speech Recognition API)
- A webcam and microphone (for Live Proctoring)

### Step 1 — Clone / Download the Project
Place all project files inside a single folder (e.g., `BrainyBEAM Final/`).

### Step 2 — Install All Dependencies
Open a terminal/PowerShell in the project directory and run:
```bash
pip install -r requirements.txt
```

This installs all core and advanced libraries automatically.

### Step 3 — Place the Dataset
Download the Kaggle dataset and place `virtual_interview_with_target.csv` in the project root directory.

If you don't have the dataset, generate synthetic data instead:
```bash
python data_generator.py
```
This creates a compatible `virtual_interview_with_target.csv` with mock data.

### Step 4 — Run EDA (Optional but Recommended)
```bash
python eda.py
```
This generates all 5 visualization plots inside the `eda_plots/` folder.

### Step 5 — Train the Model
```bash
python train_model.py
```
This will:
1. Load and preprocess the dataset
2. Train all 5 models (Linear, Random Forest, AdaBoost, Gradient Boosting, Ensemble)
3. Evaluate each on R², MAE, and RMSE
4. Save the best model, scaler, and feature list as `.pkl` files

---

## 15. How to Run

### Start the Web Application
```bash
python -m streamlit run app.py
```

> Use `python -m streamlit` (not just `streamlit`) to avoid Windows PATH issues.

### Access the App
Open your browser and navigate to:
- **Local:** http://localhost:8501
- **Network:** http://192.168.0.XXX:8501 (for other devices on the same network)

---

## 16. Output & Scoring Logic

### Manual Mode (Tabs 1–4 → Predict Performance Button)
The interviewer fills in all 14 metrics manually and clicks **"Predict Performance"**.

The ML model produces a continuous regression score which is categorized as:

| Predicted Score | Category | Color |
|-----------------|----------|-------|
| ≥ 20 | 🌟 Excellent | Green |
| ≥ 12 | 👍 Good | Blue |
| < 12 | ⚠️ Needs Improvement | Red |

**Dashboard Output:**
- **Gauge Chart** — Speedometer-style chart (0–30 range)
- **Radar Chart** — Spider web of Eye Contact, Confidence, Time Management, Network Stability, Round Score
- **Smart Suggestions** — Conditional bullet-point feedback on low-scoring metrics
- **Final Verdict** — Hiring recommendation

### Automated Mode (Tab 7 — AI Video Scorer)
Scores are derived entirely from AI analysis of the uploaded video.

**Dashboard Output:**
- 5 Metric Cards (Eye Contact, Confidence, Voice Tone, NLP Sentiment, Face Presence %)
- Plotly Gauge Chart (0–10 scale)
- Plotly Radar Chart (4 metrics)
- Smart suggestions + Verdict

---

## 17. Performance Metrics

The models are evaluated using:

| Metric | Description |
|--------|-------------|
| **R² Score** | 1.0 = perfect prediction; measures explained variance |
| **MAE (Mean Absolute Error)** | Average absolute difference between prediction and actual |
| **RMSE (Root Mean Squared Error)** | Penalizes larger errors more heavily than MAE |

The `VotingRegressor` ensemble is selected when its R² score meets or exceeds the best individual model, providing more stable and generalized predictions.

---

## 18. Future Improvements

The following enhancements are planned or can be added to extend the system:

| Improvement | Description |
|-------------|-------------|
| **Deep Learning Face Analysis** | Replace Haar Cascades with a fine-tuned CNN (e.g., DeepFace, FER+) for more accurate emotion classification (happy, sad, anxious, confident) |
| **Real-time Continuous Transcription** | Use streaming Whisper ASR instead of buffered Google STT for near-zero latency transcription |
| **Persistent Storage** | Integrate SQLite or PostgreSQL to store all interview sessions, scores, and transcripts for historical analysis |
| **Candidate Portal** | Add a separate login flow for candidates to self-submit video interviews asynchronously |
| **PDF Report Export** | Auto-generate a formatted PDF scorecard for each candidate to share with the hiring team |
| **Multi-language Support** | Extend speech recognition and NLP to support non-English candidates |
| **Body Language Analysis** | Use MediaPipe Pose to detect slouching, fidgeting, and hand gestures as additional behavioral signals |
| **Docker Deployment** | Containerize the application for one-click deployment to cloud platforms (AWS, GCP, Azure) |
| **Bias Audit Module** | Add a fairness/bias audit report that checks if scores correlate with protected attributes (age, etc.) |
| **Interviewer Dashboard** | A dedicated admin panel showing comparative analytics across multiple candidates in the same hiring round |

---

## 👥 Contributors

Developed as part of the **BrainyBEAM** AI & Machine Learning project.

## 📄 License

This project is for academic and educational purposes only.

---

*Built with ❤️ using Python, Streamlit, scikit-learn, OpenCV, and Plotly.*
