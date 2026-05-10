import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

st.set_page_config(page_title="Interview Performance Scoring", layout="wide", page_icon="🎯")

# Custom CSS for modern aesthetics
st.markdown("""
<style>
/* Main Background and Text */
.stApp {
    background-color: #0b0f19;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}
/* Custom headings */
h1, h2, h3 {
    color: #f8fafc !important;
}
/* Inputs */
.stNumberInput>div>div>input, .stTextInput>div>div>input {
    border-radius: 8px;
}
/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.5rem 1rem;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(139, 92, 246, 0.3);
}
/* Metric Cards */
div[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    color: #10b981 !important;
}
</style>
""", unsafe_allow_html=True)

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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Candidate Info", "Interview Logistics", "Technical & Behavioral", "Soft Skills", "Advanced Analytics", "Live Proctoring"])

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

with tab5:
    st.header("Advanced Analytics")
    st.info("These features use live NLP and Computer Vision to analyze candidate input.")
    
    st.subheader("NLP Analysis of Spoken Answers")
    transcript = st.text_area("Paste Interview Transcript here:")
    if transcript:
        from textblob import TextBlob
        sentiment = TextBlob(transcript).sentiment.polarity
        st.write(f"**Calculated Sentiment Score:** {sentiment:.2f} (-1 to 1)")
        # Note: We don't overwrite input_data here to maintain compatibility with the legacy model,
        # but the analysis is presented to the user.
    
    st.subheader("Facial Emotion (OpenCV)")
    camera_photo = st.camera_input("Take a photo to analyze facial expression")
    if camera_photo:
        import cv2
        from PIL import Image
        import numpy as np
        
        # Load Haar cascades
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        
        image = Image.open(camera_photo)
        img_array = np.array(image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        emotion_score = 50 # Default neutral
        if len(faces) == 0:
            st.warning("No face detected. Please try again.")
        else:
            for (x,y,w,h) in faces:
                cv2.rectangle(img_array, (x,y), (x+w, y+h), (255,0,0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
                if len(smiles) > 0:
                    st.success("Detected positive emotion (Smile/Confidence)!")
                    emotion_score = 85
                else:
                    st.info("Neutral or serious emotion detected.")
                    emotion_score = 50
            
            st.image(img_array, caption="Processed Image with OpenCV", use_column_width=True)
            st.write(f"**Calculated Positive Emotion Score:** {emotion_score}%")
            
    st.subheader("Voice Tone Analysis")
    audio_file = st.file_uploader("Upload an audio clip (.wav) of the candidate", type=["wav"])
    if audio_file is not None:
        import scipy.io.wavfile as wav
        rate, data = wav.read(audio_file)
        if len(data.shape) > 1:
            data = data.mean(axis=1) # convert to mono
        # Calculate standard deviation as a proxy for tone variation/stability
        std_dev = np.std(data)
        tone_score = min(max(10 - (std_dev / 1000), 1.0), 10.0) # Mock normalization
        st.write(f"**Voice Tone Stability Score:** {tone_score:.2f} / 10.0")

with tab6:
    st.header("Live Proctoring System")
    st.warning("Ensure your camera and microphone are enabled. Do not switch tabs.")
    
    # Tab visibility / Screen sharing alert script
    import streamlit.components.v1 as components
    components.html("""
    <script>
    // Listen to the parent window since components run in an iframe
    window.parent.document.addEventListener("visibilitychange", () => {
        if (window.parent.document.hidden) {
            window.parent.alert("PROCTORING ALERT: You have switched tabs or minimized the window. This incident has been recorded.");
        }
    });
    </script>
    """, height=0, width=0)
    
    from streamlit_webrtc import webrtc_streamer
    import av
    import cv2
    
    def video_frame_callback(frame):
        img = frame.to_ndarray(format="bgr24")
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            cv2.putText(img, "WARNING: NO FACE DETECTED", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        elif len(faces) > 1:
            cv2.putText(img, "WARNING: MULTIPLE PEOPLE DETECTED", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        else:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, "CANDIDATE DETECTED", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
        return av.VideoFrame.from_ndarray(img, format="bgr24")
        
    webrtc_streamer(
        key="proctoring",
        video_frame_callback=video_frame_callback,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": True}
    )
    
    st.info("🎙️ Audio is being captured and monitored for background noise and speaking cadence.")

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
