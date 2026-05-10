import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
import cv2
import av
import queue
import threading
import speech_recognition as sr
import scipy.io.wavfile as wav
import plotly.graph_objects as go
import tempfile
from textblob import TextBlob
from PIL import Image
from streamlit_webrtc import webrtc_streamer
from moviepy import VideoFileClip
import streamlit.components.v1 as components
import nltk

# Ensure NLTK data is downloaded for TextBlob
@st.cache_resource
def download_nltk_data():
    try:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('brown')
        nltk.download('wordnet')
        nltk.download('punkt_tab')
    except Exception as e:
        st.error(f"Error downloading NLTK data: {e}")

download_nltk_data()

st.set_page_config(page_title="Interview Performance Scoring", layout="wide", page_icon="🎯")

# Custom CSS for modern aesthetics
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

/* Main Background and Text */
.stApp {
    background: radial-gradient(circle at top, #1e1b4b, #020617);
    color: #e2e8f0;
    font-family: 'Outfit', sans-serif;
}

/* Custom headings */
h1, h2, h3 {
    color: #f8fafc !important;
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    letter-spacing: -0.5px;
}

/* Inputs and Sliders */
.stNumberInput>div>div>input, .stTextInput>div>div>input, .stTextArea textarea {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: white;
    transition: all 0.3s ease;
}
.stNumberInput>div>div>input:focus, .stTextInput>div>div>input:focus, .stTextArea textarea:focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.3);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #4f46e5, #ec4899);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 1.1rem;
    padding: 0.75rem 2rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    width: 100%;
}
.stButton>button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 20px 25px -5px rgba(236, 72, 153, 0.4), 0 10px 10px -5px rgba(236, 72, 153, 0.2);
    border: none;
    color: white;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(255,255,255,0.03);
    padding: 10px;
    border-radius: 16px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 8px;
    padding: 10px 20px;
    color: #94a3b8;
    border: 1px solid transparent;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Metric Cards & Data Expander */
div[data-testid="stMetricValue"] {
    font-size: 2.5rem !important;
    font-weight: 800;
    color: #10b981 !important;
}
.streamlit-expanderHeader {
    background-color: rgba(255,255,255,0.05);
    border-radius: 8px;
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Candidate Info", "Interview Logistics", "Technical & Behavioral", "Soft Skills", "Advanced Analytics", "Live Proctoring", "🎬 AI Video Scorer"])

# Dictionary to hold user input
input_data = {}

with tab1:
    st.header("Candidate Information")
    c1, c2 = st.columns(2)
    with c1:
        input_data['Age'] = st.number_input("Age", min_value=18, max_value=65, value=25)
    with c2:
        input_data['Education Score'] = st.number_input("Education Score (1-10)", min_value=1.0, max_value=10.0, value=7.5, step=0.1)

with tab2:
    st.header("Interview Logistics")
    c1, c2, c3 = st.columns(3)
    with c1:
        input_data['Duration'] = st.number_input("Interview Duration (mins)", min_value=10, max_value=120, value=45)
    with c2:
        input_data['Network Stability'] = st.number_input("Network Stability (1-10)", min_value=1.0, max_value=10.0, value=8.0, step=0.1)
    with c3:
        input_data['Round Score'] = st.number_input("Round Score (1-10)", min_value=1.0, max_value=10.0, value=7.0, step=0.1)

with tab3:
    st.header("Technical & Behavioral")
    c1, c2, c3 = st.columns(3)
    with c1:
        input_data['Technical Questions Answered'] = st.number_input("Technical Questions Answered (0-10)", min_value=0, max_value=10, value=5)
    with c2:
        input_data['Coding Test Score'] = st.number_input("Coding Test Score (0-100)", min_value=0, max_value=100, value=75)
    with c3:
        input_data['Behavioural Questions Answered'] = st.number_input("Behavioural Questions Answered (0-10)", min_value=0, max_value=10, value=5)

with tab4:
    st.header("Soft Skills")
    c1, c2, c3 = st.columns(3)
    with c1:
        input_data['Eye Contact Score'] = st.number_input("Eye Contact Score (1-10)", min_value=1.0, max_value=10.0, value=7.0, step=0.1)
        input_data['Filler Words Used'] = st.number_input("Filler Words Used", min_value=0, max_value=50, value=5)
    with c2:
        input_data['Confidence Score'] = st.number_input("Confidence Score (1-10)", min_value=1.0, max_value=10.0, value=7.0, step=0.1)
        input_data['Time Management Score'] = st.number_input("Time Management Score (1-10)", min_value=1.0, max_value=10.0, value=7.0, step=0.1)
    with c3:
        input_data['Speech Speed (WPM)'] = st.number_input("Speech Speed (WPM)", min_value=50, max_value=250, value=120)
        input_data['Interviewer Rating'] = st.number_input("Interviewer Rating (1-10)", min_value=1.0, max_value=10.0, value=7.0, step=0.1)

with tab5:
    st.header("Advanced Analytics")
    st.info("These features use live NLP and Computer Vision to analyze candidate input.")
    
    st.subheader("NLP Analysis of Spoken Answers")
    transcript = st.text_area("Paste Interview Transcript here:")
    if transcript:
        sentiment = TextBlob(transcript).sentiment.polarity
        st.write(f"**Calculated Sentiment Score:** {sentiment:.2f} (-1 to 1)")
        # Note: We don't overwrite input_data here to maintain compatibility with the legacy model,
        # but the analysis is presented to the user.
    
    st.subheader("Facial Emotion (OpenCV)")
    camera_photo = st.camera_input("Take a photo to analyze facial expression")
    if camera_photo:
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

with tab6:
    st.header("Live Proctoring System")
    st.warning("Ensure your camera and microphone are enabled. Do not switch tabs.")
    
    # Tab visibility / Screen sharing alert script
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
        
    class AudioProcessor:
        def __init__(self):
            self.audio_frames = []
            self.lock = threading.Lock()
            self.recognizer = sr.Recognizer()
            self.latest_transcript = ""

        def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
            data = frame.to_ndarray()
            # Still compute std_dev for voice tone stability feature
            std_dev = np.std(data)

            # Store raw audio data for transcription
            with self.lock:
                self.audio_frames.append(data)
            
            return frame
            
    webrtc_ctx = webrtc_streamer(
        key="proctoring",
        video_frame_callback=video_frame_callback,
        audio_receiver_size=256,
        audio_processor_factory=AudioProcessor,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": True}
    )
    st.info("🎙️ Live Voice Tone Analysis & Transcription Active: Audio is continuously monitored for speaking cadence and converted to text.")
    
    if "transcript" not in st.session_state:
        st.session_state["transcript"] = ""

    st.subheader("📝 Live Interview Transcript")
    transcript_container = st.empty()
    transcript_container.text_area("Live Transcript:", value=st.session_state["transcript"], height=150, key="transcript_display")

    if webrtc_ctx.state.playing:
        if st.button("Transcribe Current Audio Buffer"):
            if webrtc_ctx.audio_processor:
                with webrtc_ctx.audio_processor.lock:
                    frames = webrtc_ctx.audio_processor.audio_frames
                    webrtc_ctx.audio_processor.audio_frames = []
                
                if len(frames) > 0:
                    # Concatenate audio frames
                    audio_data = np.concatenate(frames)
                    if len(audio_data.shape) > 1:
                        audio_data = audio_data.mean(axis=1) # to mono
                    audio_data = audio_data.astype(np.int16)
                    
                    # Save to temp file
                    temp_wav = "temp_transcript.wav"
                    wav.write(temp_wav, 48000, audio_data)
                    
                    # Transcribe
                    try:
                        with sr.AudioFile(temp_wav) as source:
                            audio_content = recognizer.record(source)
                            text = recognizer.recognize_google(audio_content)
                            st.session_state["transcript"] += " " + text
                            transcript_container.text_area("Live Transcript:", value=st.session_state["transcript"], height=150)
                            st.success(f"Recognized: {text}")
                    except sr.UnknownValueError:
                        st.warning("Could not understand audio chunk.")
                    except sr.RequestError as e:
                        st.error(f"Speech Recognition error: {e}")
                    except Exception as e:
                        st.error(f"Error processing audio: {e}")
                else:
                    st.info("No audio data collected yet. Speak into the microphone.")

    st.subheader("🖥️ Screen Observation")
    st.write("To prevent unauthorized assistance, the candidate's screen must be shared and monitored.")
    
    components.html("""
    <div style="text-align: center; font-family: sans-serif; color: white;">
        <button id="startBtn" style="background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-bottom: 10px; font-weight: bold;">Start Screen Share</button>
        <video id="screen-video" autoplay playsinline style="width: 100%; border: 2px solid #ef4444; border-radius: 8px; background: #000;"></video>
    </div>
    <script>
    const videoElem = document.getElementById('screen-video');
    const startElem = document.getElementById('startBtn');
    
    startElem.addEventListener('click', async () => {
        try {
            const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
            videoElem.srcObject = stream;
            startElem.style.display = 'none'; // Hide button once sharing starts
        } catch (err) {
            console.error("Error: " + err);
            alert("You must allow screen sharing to proceed with the proctored interview.");
        }
    });
    </script>
    """, height=450)

with tab7:
    st.header("🎬 AI Automatic Video Interview Scorer")
    st.markdown("""
    Upload a recorded interview video. The AI will automatically:
    - 🎙️ **Transcribe** the candidate's speech
    - 😊 **Analyze facial expressions** frame-by-frame
    - 📊 **Score** the candidate using NLP sentiment + Computer Vision
    - 💡 **Generate** a full performance report with suggestions
    """)

    video_file = st.file_uploader("Upload Interview Video (MP4, AVI, MOV)", type=["mp4", "avi", "mov"])

    if video_file is not None:
        # Save uploaded video to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
            tmp_video.write(video_file.read())
            tmp_video_path = tmp_video.name

        st.video(tmp_video_path)

        if st.button("🚀 Analyze & Score Video"):
            with st.spinner("Analyzing video... This may take a moment."):
                
                # --- STEP 1: Extract Audio & Transcribe ---
                transcript_text = ""
                tone_score = 5.0
                try:
                    clip = VideoFileClip(tmp_video_path)
                    tmp_audio_path = tmp_video_path.replace(".mp4", "_audio.wav")
                    clip.audio.write_audiofile(tmp_audio_path, logger=None)
                    clip.close()

                    # Transcribe audio
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(tmp_audio_path) as source:
                        audio_content = recognizer.record(source)
                    try:
                        transcript_text = recognizer.recognize_google(audio_content)
                    except sr.UnknownValueError:
                        transcript_text = "(Could not transcribe audio clearly)"
                    except sr.RequestError:
                        transcript_text = "(Speech recognition service unavailable)"

                    # Voice Tone from audio
                    rate, audio_data = wav.read(tmp_audio_path)
                    if len(audio_data.shape) > 1:
                        audio_data = audio_data.mean(axis=1)
                    std_dev = np.std(audio_data)
                    tone_score = float(min(max(10 - (std_dev / 5000), 1.0), 10.0))
                    os.remove(tmp_audio_path)
                except Exception as e:
                    transcript_text = f"(Audio extraction failed: {e})"

                # --- STEP 2: Frame-by-frame Face & Smile Analysis ---
                cap = cv2.VideoCapture(tmp_video_path)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

                total_frames, face_frames, smile_frames, no_face_frames = 0, 0, 0, 0
                frame_skip = 15  # Analyze every 15th frame for speed

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    total_frames += 1
                    if total_frames % frame_skip != 0:
                        continue
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    if len(faces) == 0:
                        no_face_frames += 1
                    else:
                        face_frames += 1
                        for (x, y, w, h) in faces:
                            roi = gray[y:y+h, x:x+w]
                            smiles = smile_cascade.detectMultiScale(roi, 1.8, 20)
                            if len(smiles) > 0:
                                smile_frames += 1
                cap.release()

                analyzed = face_frames + no_face_frames
                eye_contact_score = round((face_frames / analyzed * 10), 1) if analyzed > 0 else 5.0
                confidence_score = round((smile_frames / analyzed * 10), 1) if analyzed > 0 else 5.0
                presence_pct = round((face_frames / analyzed * 100), 1) if analyzed > 0 else 0

                # --- STEP 3: NLP Sentiment ---
                sentiment_score = 0.0
                if transcript_text and not transcript_text.startswith("("):
                    blob = TextBlob(transcript_text)
                    sentiment_score = blob.sentiment.polarity  # -1 to 1

                # Map sentiment to 1-10
                nlp_score = round((sentiment_score + 1) / 2 * 10, 1)
                os.remove(tmp_video_path)

            # --- STEP 4: Display Full Report ---
            st.success("✅ Analysis Complete!")
            st.divider()

            st.subheader("📝 Auto-Generated Transcript")
            st.text_area("Candidate Speech:", transcript_text, height=120)

            st.subheader("📊 AI Performance Dashboard")
            col1, col2, col3 = st.columns(3)
            col1.metric("👁️ Eye Contact Score", f"{eye_contact_score}/10")
            col2.metric("😊 Confidence Score", f"{confidence_score}/10")
            col3.metric("🎙️ Voice Tone Stability", f"{tone_score:.1f}/10")

            col4, col5 = st.columns(2)
            col4.metric("💬 NLP Sentiment Score", f"{nlp_score}/10")
            col5.metric("🧑 Face Presence", f"{presence_pct}%")

            # Gauge chart for overall score
            overall_score = round((eye_contact_score + confidence_score + tone_score + nlp_score) / 4, 2)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=overall_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Overall AI Score", 'font': {'size': 22, 'color': 'white'}},
                gauge={
                    'axis': {'range': [0, 10], 'tickcolor': 'white'},
                    'bar': {'color': '#10b981'},
                    'steps': [
                        {'range': [0, 4], 'color': 'rgba(239,68,68,0.3)'},
                        {'range': [4, 7], 'color': 'rgba(59,130,246,0.3)'},
                        {'range': [7, 10], 'color': 'rgba(16,185,129,0.3)'}],
                    'bgcolor': 'rgba(0,0,0,0)'
                }
            ))
            fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': 'white'})

            # Radar chart
            r_labels = ['Eye Contact', 'Confidence', 'Voice Tone', 'NLP Sentiment']
            r_vals = [eye_contact_score, confidence_score, tone_score, nlp_score]
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=r_vals + [r_vals[0]],
                theta=r_labels + [r_labels[0]],
                fill='toself', line=dict(color='#ec4899')
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"),
                title=dict(text="Skills Radar", font=dict(color='white', size=20))
            )

            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(fig_gauge, use_container_width=True)
            with c2:
                st.plotly_chart(fig_radar, use_container_width=True)

            # Final verdict
            st.subheader("💡 AI Suggestions & Verdict")
            if eye_contact_score < 5:
                st.warning("- **Eye Contact**: Candidate was frequently off-camera or looking away. Suggest practicing interview presence.")
            if confidence_score < 4:
                st.warning("- **Confidence**: Low smile/positive expression detected. Candidate may benefit from mock interviews.")
            if tone_score < 5:
                st.warning("- **Voice Stability**: High variation in voice tone detected. Recommend speech coaching.")
            if nlp_score < 5:
                st.warning("- **Communication**: Negative or neutral sentiment in answers. Encourage more structured, positive responses.")
            if no_face_frames > face_frames:
                st.error("- ⚠️ **Presence Alert**: Candidate was absent from camera for more than 50% of the interview!")

            if overall_score >= 7:
                st.success(f"🌟 **Verdict: Excellent Candidate** (Score: {overall_score}/10). Strongly recommended for next round.")
            elif overall_score >= 5:
                st.info(f"👍 **Verdict: Good Candidate** (Score: {overall_score}/10). Consider with noted improvements.")
            else:
                st.error(f"⚠️ **Verdict: Needs Significant Improvement** (Score: {overall_score}/10). Not recommended at this stage.")

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
    
    # Display Result Dashboard
    st.subheader("📊 Performance Dashboard (Power BI Style)")
    st.markdown(f"### Performance Category: <span style='color:{color}'>{category}</span>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        # Gauge Chart for Final Score
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = predicted_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Predicted Final Score", 'font': {'size': 24, 'color': 'white'}},
            gauge = {
                'axis': {'range': [0, 30], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': color},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 12], 'color': 'rgba(255, 0, 0, 0.3)'},
                    {'range': [12, 20], 'color': 'rgba(0, 0, 255, 0.3)'},
                    {'range': [20, 30], 'color': 'rgba(0, 255, 0, 0.3)'}],
            }
        ))
        fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        # Radar Chart for Soft Skills Breakdown
        categories = ['Eye Contact', 'Confidence', 'Time Management', 'Network Stability', 'Round Score']
        values = [input_data['Eye Contact Score'], input_data['Confidence Score'], 
                  input_data['Time Management Score'], input_data['Network Stability'], input_data['Round Score']]
                  
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='#3b82f6')
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            title=dict(text="Skills Breakdown", font=dict(color="white", size=20))
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.subheader("💡 Actionable Suggestions")
    if input_data['Eye Contact Score'] < 6:
        st.warning("- **Eye Contact**: Needs improvement. The candidate should focus more directly on the camera.")
    if input_data['Filler Words Used'] > 15:
        st.warning("- **Communication**: High use of filler words detected. Recommend practicing structured speaking to reduce 'ums' and 'uhs'.")
    if input_data['Coding Test Score'] < 60:
        st.warning("- **Technical Skills**: Coding score is below average. Recommend further technical evaluation.")
    if input_data['Confidence Score'] < 6:
        st.warning("- **Confidence**: The candidate appeared nervous. Consider a less intimidating environment for future rounds.")
    if input_data['Speech Speed (WPM)'] < 100 or input_data['Speech Speed (WPM)'] > 160:
        st.warning("- **Pacing**: Speech speed was outside the optimal range. They may have been speaking too fast or too slow.")
        
    if predicted_score >= 20:
        st.success("🌟 Highly recommended candidate. Excellent overall performance. Fast-track to the next stage.")
    elif predicted_score >= 12:
        st.info("👍 Good candidate, but review the warnings above for potential areas of growth.")
    else:
        st.error("⚠️ Candidate requires significant improvement. Not recommended for hiring at this stage.")
    
    with st.expander("Show Raw Data Details"):
        st.json(input_data)
