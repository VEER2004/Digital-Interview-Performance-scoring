import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

st.set_page_config(page_title="Interview Performance Scoring", layout="wide", page_icon="🎯")

# Define the model paths
MODEL_PATH = "best_interview_performance_model.pkl"
SCALER_PATH = "scaler.pkl"
FEATURES_PATH = "feature_columns.pkl"

st.title("🎯 Digital Interview Performance Scoring System")
st.markdown("""
This AI-based system predicts and scores candidate interview performance using structured interview metrics.
Fill out the details below across the tabs to get a real-time prediction of the candidate's performance.
""")

# Load artifacts
@st.cache_resource
def load_artifacts():
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH) and os.path.exists(FEATURES_PATH):
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        features = joblib.load(FEATURES_PATH)
        return model, scaler, features
    else:
        return None, None, None

model, scaler, feature_cols = load_artifacts()

if model is None:
    st.error("⚠️ Model files not found. Please train the model by running 'train_model.py' first.")
    st.stop()

# Create tabs as requested
tab1, tab2, tab3, tab4 = st.tabs(["Candidate Info", "Interview Logistics", "Technical & Behavioral", "Soft Skills"])

# Dictionary to hold user input
input_data = {}

with tab1:
    st.header("Candidate Information")
    input_data['Age'] = st.number_input("Age", min_value=18, max_value=65, value=25)
    input_data['Education Score'] = st.slider("Education Score", min_value=1.0, max_value=10.0, value=7.5, step=0.1)

with tab2:
    st.header("Interview Logistics")
    input_data['Duration'] = st.slider("Interview Duration (mins)", min_value=10, max_value=120, value=45)
    input_data['Network Stability'] = st.slider("Network Stability (1-10)", min_value=1.0, max_value=10.0, value=8.0, step=0.1)
    input_data['Round Score'] = st.slider("Round Score", min_value=1.0, max_value=10.0, value=7.0, step=0.1)

with tab3:
    st.header("Technical & Behavioral")
    input_data['Technical Questions Answered'] = st.slider("Technical Questions Answered", min_value=0, max_value=10, value=5)
    input_data['Coding Test Score'] = st.slider("Coding Test Score", min_value=0, max_value=100, value=75)
    input_data['Behavioural Questions Answered'] = st.slider("Behavioural Questions Answered", min_value=0, max_value=10, value=5)

with tab4:
    st.header("Soft Skills")
    input_data['Eye Contact Score'] = st.slider("Eye Contact Score", min_value=1.0, max_value=10.0, value=7.0, step=0.1)
    input_data['Confidence Score'] = st.slider("Confidence Score", min_value=1.0, max_value=10.0, value=7.0, step=0.1)
    input_data['Speech Speed (WPM)'] = st.slider("Speech Speed (WPM)", min_value=50, max_value=250, value=120)
    input_data['Filler Words Used'] = st.slider("Filler Words Used", min_value=0, max_value=50, value=5)
    input_data['Time Management Score'] = st.slider("Time Management Score", min_value=1.0, max_value=10.0, value=7.0, step=0.1)
    input_data['Interviewer Rating'] = st.slider("Interviewer Rating", min_value=1.0, max_value=10.0, value=7.0, step=0.1)

st.divider()

# Prediction Logic
if st.button("Predict Performance", type="primary"):
    # Convert input to DataFrame ensuring correct column order
    input_df = pd.DataFrame([input_data])
    input_df = input_df[feature_cols]  # Reorder columns as expected by the model
    
    # Scale the input
    input_scaled = scaler.transform(input_df)
    
    # Predict
    predicted_score = model.predict(input_scaled)[0]
    
    # Categorize
    if predicted_score >= 20:
        category = "Excellent 🌟"
        color = "green"
    elif predicted_score >= 12:
        category = "Good 👍"
        color = "blue"
    else:
        category = "Needs Improvement ⚠️"
        color = "red"
    
    # Display Result
    st.subheader("Prediction Result")
    st.markdown(f"### Predicted Score: **{predicted_score:.2f}**")
    st.markdown(f"### Performance Category: <span style='color:{color}'>{category}</span>", unsafe_allow_html=True)
    
    with st.expander("Show Details"):
        st.json(input_data)
