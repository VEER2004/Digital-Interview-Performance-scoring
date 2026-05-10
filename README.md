# Digital Interview Performance Scoring System

This project is an AI-based system that predicts and scores candidate interview performance using structured interview metrics, developed in Python and Streamlit.

## Setup Instructions

1. **Install Dependencies**
   Open a terminal in the project folder and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate the Dataset (if you don't have the Kaggle dataset)**
   If you don't have the `virtual_interview_with_target.csv` file, generate a mock dataset by running:
   ```bash
   python data_generator.py
   ```

3. **Train the Model**
   Run the model training script to clean the data, select features, and train a Linear Regression model.
   ```bash
   python train_model.py
   ```
   This will save `best_interview_performance_model.pkl`, `scaler.pkl`, and `feature_columns.pkl`.

4. **Run the Streamlit Web App**
   Start the interactive Streamlit application to predict scores in real-time.
   ```bash
   streamlit run app.py
   ```

## Features
The web app is categorized into four tabs:
- **Candidate Info**: Age, Education Score
- **Interview Logistics**: Duration, Network Stability, Round Score
- **Technical & Behavioral**: Technical Questions Answered, Coding Test Score, Behavioural Questions Answered
- **Soft Skills**: Eye Contact Score, Confidence Score, Speech Speed (WPM), Filler Words Used, Time Management Score, Interviewer Rating

## Output Logic
The model predicts a regression score which is then categorized as:
- **Score ≥ 20** → Excellent
- **Score ≥ 12** → Good
- **Else** → Needs Improvement
