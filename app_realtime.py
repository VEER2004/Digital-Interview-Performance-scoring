"""
Real-time interview analysis Streamlit app.
Combines video and audio analysis for live interview metrics.
"""

import streamlit as st
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict
import sys
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from real_time_video import InterviewVideoProcessor
from facial_analysis import FacialExpressionAnalyzer, EmotionScoreCalculator
from speech_analysis import InterviewAudioAnalyzer

# Page config
st.set_page_config(
    page_title="Real-time Interview Analysis",
    page_icon="📹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .positive { color: #0f9d58; font-weight: bold; }
    .negative { color: #d33b27; font-weight: bold; }
    .neutral { color: #ea8600; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)


def initialize_session():
    """Initialize Streamlit session variables."""
    if 'video_processor' not in st.session_state:
        st.session_state.video_processor = None
    if 'audio_analyzer' not in st.session_state:
        st.session_state.audio_analyzer = None
    if 'recording' not in st.session_state:
        st.session_state.recording = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'frames_data' not in st.session_state:
        st.session_state.frames_data = []
    if 'expression_analyzer' not in st.session_state:
        st.session_state.expression_analyzer = FacialExpressionAnalyzer()


def draw_metrics_row(label, value, unit="", benchmark_range=None):
    """Draw a metric with optional benchmark."""
    col = st.columns(1)[0]
    with col:
        if benchmark_range:
            if isinstance(value, (int, float)):
                min_val, max_val = benchmark_range
                if min_val <= value <= max_val:
                    status = "✅"
                else:
                    status = "⚠️"
            else:
                status = "ℹ️"
        else:
            status = ""
        
        st.metric(label, f"{status} {value} {unit}".strip())


def main():
    """Main app logic."""
    initialize_session()
    
    # Header
    st.title("🎥 Real-Time Interview Analysis Dashboard")
    st.markdown("Analyze facial expressions, eye contact, speech patterns, and sentiment in real-time.")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        analysis_mode = st.radio(
            "Analysis Mode",
            ["📹 Webcam (Real-time)", "📄 Upload Video File", "📊 Batch Analysis"],
            help="Choose how to provide video input"
        )
        
        st.subheader("Video Settings")
        enable_visualizations = st.checkbox("Show visualizations", value=True)
        confidence_threshold = st.slider(
            "Face detection confidence",
            0.1, 1.0, 0.5,
            help="Higher = stricter face detection"
        )
        
        st.subheader("Analysis Metrics")
        col1, col2 = st.columns(2)
        with col1:
            analyze_expressions = st.checkbox("Facial Expressions", value=True)
        with col2:
            analyze_speech = st.checkbox("Speech/Audio", value=True)
        
        st.divider()
        
        if st.button("📋 View Documentation", use_container_width=True):
            st.info("""
            **Real-time Analysis Features:**
            
            1. **Facial Analysis**
               - Eye contact detection (0-1 score)
               - Expression recognition (smile, neutral, frown, etc.)
               - Engagement metrics (0-20 scale)
            
            2. **Speech Analysis**
               - Speaking rate (words per minute)
               - Pitch variance and spectral properties
               - Filler word detection
               - Sentiment analysis
            
            3. **Performance Scoring**
               - Combined interview score (0-20)
               - Real-time metrics update
               - Historical trend analysis
            """)
    
    # Main content
    if analysis_mode == "📹 Webcam (Real-time)":
        st.header("Live Webcam Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Video Feed")
            video_placeholder = st.empty()
            
            # Control buttons
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                if st.button("▶️ Start Analysis", use_container_width=True):
                    st.session_state.recording = True
                    st.session_state.start_time = datetime.now()
                    st.session_state.video_processor = InterviewVideoProcessor(source=0)
            
            with btn_col2:
                if st.button("⏸️ Stop Analysis", use_container_width=True):
                    st.session_state.recording = False
            
            with btn_col3:
                if st.button("🔄 Reset", use_container_width=True):
                    st.session_state.frames_data = []
                    st.session_state.recording = False
        
        with col2:
            st.subheader("Session Info")
            if st.session_state.start_time:
                elapsed = datetime.now() - st.session_state.start_time
                st.metric("Duration", f"{elapsed.seconds}s")
                st.metric("Frames Analyzed", len(st.session_state.frames_data))
            else:
                st.info("No active session")
        
        # Live analysis loop
        if st.session_state.recording and st.session_state.video_processor:
            if not st.session_state.video_processor.video_capture.open():
                st.error("Cannot access webcam. Please check permissions.")
                st.session_state.recording = False
            else:
                st.info("🔴 Recording... (Press 'Stop Analysis' to finish)")
                
                # Analysis loop
                frame_count = 0
                max_frames = 150  # Limit for demo
                
                progress_bar = st.progress(0)
                frame_placeholder = st.empty()
                metrics_placeholder = st.empty()
                
                while st.session_state.recording and frame_count < max_frames:
                    success, frame = st.session_state.video_processor.video_capture.read_frame()
                    
                    if not success:
                        st.warning("Lost video source")
                        break
                    
                    # Process frame
                    analysis = st.session_state.video_processor.process_frame(frame)
                    st.session_state.frames_data.append(analysis)
                    
                    # Display frame with overlays
                    display_frame = analysis['frame_with_overlay'].copy()
                    
                    # Add metrics overlay
                    h, w = display_frame.shape[:2]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    
                    metrics_text = [
                        f"Eye Contact: {analysis['eye_contact_score']:.2f}",
                        f"Faces: {analysis['faces_detected']}",
                        f"Confidence: {analysis['confidence']:.2f}",
                        f"Gaze: {analysis['gaze_direction']}"
                    ]
                    
                    y_offset = 30
                    for i, text in enumerate(metrics_text):
                        cv2.putText(display_frame, text, (10, y_offset + i * 25),
                                  font, 0.6, (0, 255, 0), 2)
                    
                    # Display frame
                    frame_placeholder.image(display_frame, channels="BGR", use_column_width=True)
                    
                    frame_count += 1
                    progress_bar.progress(frame_count / max_frames)
                
                st.session_state.video_processor.release()
        
        # Show summary after recording
        if st.session_state.frames_data and not st.session_state.recording:
            st.divider()
            st.subheader("📊 Session Summary")
            
            metrics_data = [
                'faces_detected', 'eye_contact_score', 'confidence',
                'looking_at_camera', 'face_centered'
            ]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_eye_contact = np.mean([f['eye_contact_score'] for f in st.session_state.frames_data])
                st.metric("Avg Eye Contact", f"{avg_eye_contact:.2f}/1.0",
                         delta="Good" if avg_eye_contact > 0.6 else "Needs Improvement")
            
            with col2:
                avg_confidence = np.mean([f['confidence'] for f in st.session_state.frames_data])
                st.metric("Avg Face Confidence", f"{avg_confidence:.2f}",
                         delta="High" if avg_confidence > 0.7 else "Low")
            
            with col3:
                camera_pct = sum(1 for f in st.session_state.frames_data if f['looking_at_camera']) / len(st.session_state.frames_data) * 100
                st.metric("Looking at Camera", f"{camera_pct:.0f}%",
                         delta="Engaged" if camera_pct > 70 else "Unfocused")
            
            with col4:
                centered_pct = sum(1 for f in st.session_state.frames_data if f['face_centered']) / len(st.session_state.frames_data) * 100
                st.metric("Face Centered", f"{centered_pct:.0f}%")
            
            # Plot trend
            st.subheader("📈 Eye Contact Trend")
            df = pd.DataFrame({
                'Frame': range(len(st.session_state.frames_data)),
                'Eye Contact Score': [f['eye_contact_score'] for f in st.session_state.frames_data],
                'Confidence': [f['confidence'] for f in st.session_state.frames_data]
            })
            
            fig = px.line(df, x='Frame', y=['Eye Contact Score', 'Confidence'],
                         title="Eye Contact & Confidence Over Time",
                         labels={'value': 'Score', 'variable': 'Metric'})
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_mode == "📄 Upload Video File":
        st.header("Batch Video Analysis")
        
        uploaded_file = st.file_uploader("Upload a video file", type=['mp4', 'avi', 'mov'])
        
        if uploaded_file:
            # Save uploaded file
            video_path = Path(f"/tmp/{uploaded_file.name}")
            video_path.write_bytes(uploaded_file.getbuffer())
            
            st.info(f"Analyzing: {uploaded_file.name}")
            st.info("Feature: Video file analysis coming in Phase 2")
    
    elif analysis_mode == "📊 Batch Analysis":
        st.header("Batch Interview Analysis")
        
        st.info("""
        **Batch Mode Features:**
        - Analyze multiple interview videos
        - Compare candidates across metrics
        - Generate performance reports
        - Export results to CSV/Power BI
        
        *Coming in Phase 2 implementation*
        """)
    
    # Footer
    st.divider()
    st.markdown("""
    ---
    **Enhancement Roadmap:**
    - ✅ Phase 1: Real-time video + facial detection (current)
    - ⏳ Phase 2: Speech analysis + sentiment
    - ⏳ Phase 3: Body language + pose estimation
    - ⏳ Phase 4: Integration + live dashboard
    """)


if __name__ == "__main__":
    main()
