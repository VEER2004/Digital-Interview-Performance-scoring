# Industrial Internship Report

**BrainyBeam Info-Tech Pvt. Ltd.**

*Submitted by*
**VIR K. GUSAI**
**12202110501063**

*In partial fulfillment for the award of the degree of*
**BACHELOR OF TECHNOLOGY**
*in*
**Computer Science and Engineering (IoT)**
**G H Patel College of Engineering & Technology**

The Charutar Vidya Mandal (CVM) University, Vallabh Vidyanagar – 388120
May 2026

---

# Table of Contents

1. [Overview of the Company](#1-overview-of-the-company)
2. [Introduction to Project](#2-introduction-to-project)
3. [System Analysis](#3-system-analysis)
4. [System Design](#4-system-design)
5. [Implementation](#5-implementation)
6. [Demonstration](#6-demonstration)
7. [Testing](#7-testing)
8. [Conclusion](#8-conclusion)
9. [References](#9-references)

---

## 1. Overview of the Company

### 1.1 Company Profile

BrainyBeam Info-Tech Pvt. Ltd. is an innovative technology solutions provider specializing in Machine Learning, Data Science, and modern Web Development. The company focuses on bridging the gap between academic theory and industry requirements by building intelligent, scalable, and automated solutions. BrainyBeam is dedicated to fostering young talent through rigorous industrial internships while delivering cutting-edge software to clients globally.

### 1.2 Different Departments of The Company

- **Data Science & AI Division**: Focuses on developing predictive models, computer vision applications, and NLP pipelines.
- **Web Development**: Responsible for full-stack application development, API integration, and cloud deployment.
- **Human Resources (HR)**: Manages internal recruitment, employee engagement, and internship programs.

---

## 2. Introduction to Project

### 2.1 Internship Summary

During the internship at BrainyBeam Info-Tech Pvt. Ltd., the primary assignment was to architect and develop the **Digital Interview Performance Scoring System**. This project aims to revolutionize the HR recruitment process by introducing an unbiased, AI-driven evaluation framework. The system processes both structured data (like test scores) and unstructured data (live video, audio, text) to assess candidates automatically.

### 2.2 Purpose

Traditional interviewing is inherently subjective. Interviewers can be influenced by unconscious biases, fatigue, and varying personal standards. The purpose of this project is to build a standardized, objective evaluation tool that scores candidates uniformly based on quantifiable behavioral and technical metrics.

### 2.3 Objective

The objective is to develop a complete end-to-end web application that:

1. Employs Supervised Machine Learning to predict an overall performance score based on structured metrics.
2. Integrates real-time WebRTC for live candidate proctoring.
3. Utilizes Computer Vision (OpenCV) to detect facial presence and positive expressions (smiles).
4. Employs NLP (TextBlob) and Speech Recognition to transcribe and analyze the sentiment of verbal responses.
5. Computes voice tone stability using audio waveform analysis.
6. Generates a comprehensive dashboard (Plotly) for HR decision-making.

### 2.4 Scope

The system is designed for use by HR professionals and technical recruiters. It supports:

- **Live Proctoring Mode:** Real-time analysis of webcam and microphone feeds during a live session.
- **Asynchronous AI Video Scorer:** Uploading a pre-recorded interview video for automated analysis.
  The system currently focuses on predicting scores and categorizing candidates (Excellent, Good, Needs Improvement) without making final hiring decisions autonomously.

### 2.5 Technology and Literature Review

#### 2.5.1 Technology Stack Summary

- **Frontend & UI:** Streamlit, CSS, Plotly (for interactive dashboards).
- **Machine Learning Core:** Scikit-Learn (Random Forest, Gradient Boosting, Voting Ensemble), Pandas, NumPy.
- **Computer Vision:** OpenCV (Haar Cascades for face and smile detection).
- **Natural Language Processing:** TextBlob (Sentiment Analysis), SpeechRecognition (Speech-to-text).
- **Audio Processing:** SciPy, PyAudio, MoviePy (Audio extraction from video).
- **Live Streaming/Proctoring:** Streamlit-WebRTC, WebRTC (av, tornado).

#### 2.5.2 Model Specifications

A `VotingRegressor` ensemble model was selected. It combines predictions from:

- Linear Regression (Baseline)
- Random Forest Regressor (Non-linear interactions)
- AdaBoost Regressor
- Gradient Boosting Regressor
  The models were trained on 14 engineered features (Age, Education Score, Coding Test Score, Speech Speed, etc.).

#### 2.5.3 API & Data Sources

- **Training Data:** Kaggle's "Virtual Interview Performance Dataset" (`virtual_interview_with_target.csv`).
- **Speech API:** Google Speech Recognition API (via `speech_recognition` library).

---

## 3. System Analysis

### 3.1 Problem Definition

The manual interviewing process is unscalable for high-volume recruitment. Identifying soft skills (confidence, communication, eye contact) is highly subjective. Furthermore, verifying candidate integrity during remote interviews is difficult without specialized proctoring tools.

### 3.2 Requirements of the Proposed System

The system requires:

1. A robust ML model capable of accurate continuous regression prediction.
2. Low-latency processing of live video and audio streams in the browser.
3. Integration of multiple distinct AI disciplines (CV, NLP, Audio Signal Processing).
4. A highly visual, easy-to-interpret Power BI-style dashboard.

### 3.3 Main Modules Developed

1. **Data Preprocessing & EDA Module:** Cleans the dataset and generates correlation/distribution plots.
2. **Model Training Pipeline:** Dynamically selects the best regression ensemble and persists artifacts (`.pkl`).
3. **Manual Scoring Interface (Tabs 1-4):** Collects 14 exact metrics from the interviewer.
4. **Advanced Analytics Module:** Individual tools for NLP sentiment, image-based face detection, and static audio tone analysis.
5. **Live Proctoring Module:** Real-time WebRTC face tracking, live transcription, and screen sharing with tab-switching cheat detection.
6. **AI Video Scorer Module:** Fully automated asynchronous processing of uploaded `.mp4` video files.
7. **Visualization Dashboard:** Generates gauge charts, radar charts, and actionable text suggestions.

---

## 4. System Design

### 4.1 Architecture Diagram

The system is designed with a hybrid frontend-backend architecture utilizing Streamlit as the central orchestrator.

1. **Presentation Layer (Browser):** Handles user inputs, WebRTC streams, and Plotly charts. Injects JavaScript for screen sharing and DOM visibility cheat-detection.
2. **Application Layer (Python/Streamlit):** Routes user tabs, caches ML models (`@st.cache_resource`), and manages state.
3. **AI Processing Layer:**
   - *Video/Frame Callbacks:* Passes frames to OpenCV.
   - *Audio/Stream Callbacks:* Buffers audio for Google STT and calculates Standard Deviation via Numpy/Scipy.
4. **Data/Inference Layer:** Receives structured data, scales it using `StandardScaler`, and predicts using the `VotingRegressor`.

---

## 5. Implementation

### 5.1 Machine Learning Pipeline Implementation

The `train_model.py` script uses `train_test_split` (80/20). It initializes four individual regressors. It then builds a `VotingRegressor`. The R2 score, MAE, and RMSE are calculated for all models. If the ensemble outperforms the best base model, the ensemble is saved via `joblib`.

### 5.2 Real-time Proctoring Implementation

The `streamlit-webrtc` library is used to handle real-time communications.

- A `video_frame_callback` intercepts frames, converts to grayscale, applies `haarcascade_frontalface_default.xml`, draws bounding boxes, and returns the annotated frame.
- An `AudioProcessor` class locks and appends `av.AudioFrame` arrays into a buffer. When the user clicks "Transcribe", the buffer is dumped to a `.wav` file and processed by `SpeechRecognition`.

### 5.3 Automated Video Scoring Implementation

The `moviepy` library extracts the `.wav` audio track from the uploaded video. `OpenCV` reads the video via `cv2.VideoCapture()`. To maintain performance, the system skips frames, analyzing only every 15th frame for faces and smiles to calculate the "Eye Contact" and "Confidence" scores.

---

## 6. Demonstration

The developed application features a premium dark-themed UI (radial gradient background `#1e1b4b` to `#020617`).

- **Forms:** Inputs are structured in responsive 2 and 3-column layouts to minimize scrolling.
- **Proctoring:** The WebRTC component displays the live webcam feed with green bounding boxes tracking the candidate's face.
- **Dashboards:** Upon clicking "Predict Performance", a massive Gauge Chart displays the final score (e.g., 24/30), accompanied by a blue Radar Chart mapping Soft Skills breakdown.

---

## 7. Testing

### 7.1 Unit Testing

- **Model Accuracy:** The ML pipeline was tested against the 20% test holdout set, ensuring an R2 score above baseline expectations.
- **Audio Conversion:** Verified that stereo audio arrays from WebRTC are properly flattened to mono using `.mean(axis=1)` before processing.

### 7.2 System Testing

- **Cheat Detection Trigger:** Tested the JavaScript `visibilitychange` listener. Switching browser tabs successfully triggers the browser `alert()` modal.
- **Live Video Latency:** Monitored WebRTC streaming locally. The frame-dropping algorithm ensures the UI remains responsive even when face detection is active.

---

## 8. Conclusion

The **Digital Interview Performance Scoring System** successfully demonstrates the integration of traditional supervised machine learning with modern generative and real-time AI techniques. By combining CV, NLP, and regression, the system provides a holistic, bias-reduced view of a candidate's capabilities. The addition of the "AI Video Scorer" proves that the system can scale to handle asynchronous interviews, saving immense time for HR departments.

### Future Enhancements

- **Deep Learning Vision:** Upgrading from Haar Cascades to a Convolutional Neural Network (e.g., DeepFace) for granular emotion detection.
- **Streaming ASR:** Replacing buffered Google STT with a real-time streaming model like Whisper.
- **Database Integration:** Adding PostgreSQL to persist interview scores and transcripts historically.

---

## 9. References

1. Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR.
2. Bradski, G. (2000). The OpenCV Library. Dr. Dobb's Journal of Software Tools.
3. Loria, S. (2018). textblob Documentation. Release 0.15, 2.
4. Streamlit Documentation: https://docs.streamlit.io/
5. Kaggle Dataset: Virtual Interview Performance Dataset.
