# 🚀 Phase 1 Implementation Guide: Real-Time Video & Facial Detection

## Overview

**What's New**: Complete real-time interview video analysis system with:

- ✅ Live webcam streaming
- ✅ Facial detection & expression recognition
- ✅ Eye contact analysis
- ✅ Real-time metrics dashboard
- ✅ Session recording & playback
- ✅ Foundation for Phases 2-4

**Status**: Phase 1 COMPLETE ✨

---

## 📦 Installation & Setup

### 1. Install New Dependencies

All packages are now in `requirements.txt`. The installation is automated:

```bash
cd c:\Users\Vir\Desktop\interview_performance_project\interview_performance_project

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install all packages
pip install -r requirements.txt --upgrade
```

**New Packages Added:**

- `opencv-python` - Video capture & frame processing
- `mediapipe` - Real-time face detection & landmarks
- `librosa` - Audio processing (for Phase 2)
- `speech_recognition` - Transcription (for Phase 2)
- `transformers` & `torch` - NLP/sentiment models (for Phase 2)
- `sounddevice`, `soundfile` - Audio I/O (for Phase 2)

### 2. Verify Installation

```bash
# Test imports
python -c "import cv2; import mediapipe; import librosa; print('✅ All imports successful')"
```

---

## 🎬 New Files Created

### Core Modules (src/)

| File                     | Purpose                                  | Key Classes                                                                   |
| ------------------------ | ---------------------------------------- | ----------------------------------------------------------------------------- |
| `src/real_time_video.py` | Video capture & facial detection         | `RealTimeVideoCapture`, `FacialDetectionProcessor`, `InterviewVideoProcessor` |
| `src/facial_analysis.py` | Expression recognition & emotion scoring | `FacialExpressionAnalyzer`, `EmotionScoreCalculator`                          |
| `src/speech_analysis.py` | Audio analysis & speech metrics          | `RealTimeAudioCapture`, `SpeechMetricsCalculator`, `SentimentAnalyzer`        |

### Interface

| File              | Purpose                                           |
| ----------------- | ------------------------------------------------- |
| `app_realtime.py` | **NEW** Streamlit real-time dashboard (use this!) |
| `app.py`          | Original batch prediction interface (still works) |

---

## 🚀 Quick Start Guide

### Option 1: Real-Time Vide Analysis (Recommended)

```bash
# Navigate to project directory
cd c:\Users\Vir\Desktop\interview_performance_project\interview_performance_project

# Activate venv
.\venv\Scripts\Activate.ps1

# Start real-time dashboard
.\venv\Scripts\python.exe -m streamlit run app_realtime.py
```

**Browser opens at**: `http://localhost:8501`

### Option 2: Batch Prediction (Original)

```bash
# Still works - analyze pre-recorded interview data
.\venv\Scripts\python.exe -m streamlit run app.py
```

**Browser opens at**: `http://localhost:8502`

---

## 📊 Phase 1 Features

### A. Real-Time Facial Detection

**What it does:**

- Detects face in video stream
- Tracks multiple people
- Provides confidence scores per frame

**Code Example:**

```python
from src.real_time_video import InterviewVideoProcessor

processor = InterviewVideoProcessor(source=0)  # 0 = webcam

if processor.video_capture.open():
    success, frame = processor.video_capture.read_frame()
    analysis = processor.process_frame(frame)

    print(f"Faces detected: {analysis['faces_detected']}")
    print(f"Eye contact score: {analysis['eye_contact_score']:.2f}")
    print(f"Face centered: {analysis['face_centered']}")
```

### B. Eye Contact Analysis

**What it measures:**

- Face position relative to center
- Gaze direction (left, right, center, up, down)
- Eye contact confidence (0-1)

**Output:**

```python
{
    'eye_contact_score': 0.85,  # 0-1 (higher = better)
    'looking_at_camera': True,
    'face_centered': True,
    'gaze_direction': 'forward',
    'face_position': 'centered'
}
```

### C. Facial Expression Recognition

**What it detects:**

- Smile 😊
- Neutral 😐
- Frown 😞
- Surprise 😮
- Anger 😠
- Fear 😨
- Disgust 🤢
- Sadness 😢

**Code Example:**

```python
from src.facial_analysis import FacialExpressionAnalyzer

analyzer = FacialExpressionAnalyzer()

# After getting landmarks from face detection
expressions = analyzer.detect_expressions(landmarks)

print(f"Primary expression: {expressions['primary_expression']}")
print(f"Smile confidence: {expressions['smile']:.2f}")
```

### D. Interview Performance Scoring

**Converts metrics to 0-20 scale:**

```python
from src.facial_analysis import EmotionScoreCalculator

metrics = {
    'smile_frequency': 0.3,
    'positive_expression_pct': 45,
    'negative_expression_pct': 10,
    'neutral_expression_pct': 45
}

score = EmotionScoreCalculator.calculate_expression_score(metrics)
# Returns: 12.5 (0-20)
```

### E. Session Statistics

**Captured in real-time:**

```python
stats = processor.get_session_stats()

# Output:
{
    'total_frames_analyzed': 450,
    'avg_faces_detected': 1.0,
    'avg_eye_contact_score': 0.72,
    'avg_confidence': 0.95,
    'looking_at_camera_pct': 78.0,
    'face_centered_pct': 65.0
}
```

---

## 📈 Dashboard Metrics

### Real-Time Display

The `app_realtime.py` dashboard shows:

1. **Video Feed**
   - Live video with face bounding boxes
   - Overlay metrics (eye contact, confidence, gaze direction)
   - Frame display with detections

2. **Session Information**
   - Duration (elapsed time)
   - Frames analyzed count
   - Real-time progress bar

3. **Live Metrics**
   - Average eye contact score
   - Average face confidence
   - Looking at camera percentage
   - Face centered percentage

4. **Trend Analysis**
   - Eye contact score over time (line chart)
   - Confidence trend over time
   - Expression distribution

### Sample Output

```
Duration: 45s
Frames Analyzed: 450
Avg Eye Contact: 0.72/1.0 (Good ✅)
Avg Confidence: 0.95 (High ✅)
Looking at Camera: 78% (Engaged ✅)
Face Centered: 65% ⚠️
```

---

## 🔧 Configuration Options

### Video Settings

```python
# Webcam resolution
processor = InterviewVideoProcessor(source=0)
processor.video_capture.resolution = (1280, 720)  # 720p

# Higher FPS = smoother but more processing
processor.video_capture.fps = 30  # frames per second

# Face detection confidence threshold
# Higher = stricter detection (fewer false positives)
confidence_threshold = 0.5  # Range: 0.1-1.0
```

### Expression Analysis

```python
# Customize expression sensitivity
analyzer = FacialExpressionAnalyzer()

# Adjust how much history to keep
analyzer.history_size = 100  # Frames to remember
```

---

## 📋 Integration with Existing System

### Connecting to ML Model

Phase 1 provides **raw metrics**. Phase 2+ will integrate these into your ML pipeline:

```python
import joblib
from src.real_time_video import InterviewVideoProcessor
from src.facial_analysis import EmotionScoreCalculator

# Load trained model
model = joblib.load('artifacts/best_interview_performance_model.joblib')

# Get real-time video metrics
processor = InterviewVideoProcessor()
# ... capture video ...
analysis = processor.process_frame(frame)

# Create feature vector from metrics
# In Phase 2: combine with audio/speech metrics
features = [
    analysis['eye_contact_score'],  # Eye Contact Score
    analysis['confidence'],  # Face Confidence
    # ... + other ML features ...
]

# Predict performance
prediction = model.predict([features])
print(f"Performance Score: {prediction[0]:.1f}/20")
```

---

## 🎯 Use Cases

### 1. Interview Recording & Analysis

```
1. Click "Start Analysis"
2. Conduct interview (candidate appears on webcam)
3. Click "Stop Analysis"
4. View metrics summary and trends
5. Export results
```

### 2. Candidate Comparison

Multiple candidates' same metrics side-by-side:

- Average eye contact
- Expression patterns
- Engagement consistency

### 3. Interview Coaching

Real-time feedback:

- "Maintain more eye contact"
- "Vary your expressions more"
- "Face feels centered"

---

## ⚠️ Known Limitations (Phase 1)

| Limitation                  | Workaround                      | Phase   |
| --------------------------- | ------------------------------- | ------- |
| No audio analysis yet       | Use with manual speech scoring  | Phase 2 |
| No body language detection  | Only facial analysis            | Phase 3 |
| No live engagement tracking | Post-session metrics            | Phase 4 |
| No sentiment analysis       | Planned in Phase 2              | Phase 2 |
| Single face only            | RedesignedWill support multiple | Future  |
| No movement tracking        | Body pose coming Phase 3        | Phase 3 |

---

## 🧪 Testing

### Test 1: Webcam Feed

```bash
python -c "
from src.real_time_video import InterviewVideoProcessor
processor = InterviewVideoProcessor(0)
if processor.video_capture.open():
    print('✅ Webcam accessible')
else:
    print('❌ Webcam not accessible')
"
```

### Test 2: Face Detection

```bash
python -c "
import mediapipe as mp
print(f'✅ MediaPipe version: {mp.__version__}')
"
```

### Test 3: Full Pipeline

```bash
# Run this Python script to test full pipeline
python -c "
from src.real_time_video import InterviewVideoProcessor
from src.facial_analysis import FacialExpressionAnalyzer

print('✅ All imports successful')
processor = InterviewVideoProcessor(0)
analyzer = FacialExpressionAnalyzer()
print('✅ Pipeline initialized')
"
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'mediapipe'"

**Solution:**

```bash
.\venv\Scripts\pip install mediapipe --upgrade
```

### Error: "Cannot access webcam"

**Solutions:**

1. Check webcam in Device Manager
2. Grant permission in Windows Settings
3. If using in VM: ensure video passthrough enabled
4. Try another video source (iPhone camera app via USB)

### Error: "No faces detected"

**Solutions:**

1. Ensure good lighting (face detection needs ~500-1000 lux)
2. Face should be 30cm - 1m from camera
3. Try different angles
4. Lower confidence threshold: `confidence_threshold = 0.3`

### Slow performance < 15 FPS

**Solutions:**

1. Lower video resolution: `(640, 480)` instead of `(1280, 720)`
2. Skip frames: Process every 2nd frame
3. Reduce model complexity (Phase 2+)
4. Use GPU (if available): CUDA/GPU acceleration

---

## 📦 Architecture Diagram

```
┌─────────────────────────────────────────────┐
│         app_realtime.py (Streamlit)         │
│       Real-time Dashboard Interface         │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────────┐  ┌─▼──────────────────┐
│ Real-time Video │  │ Audio Capture      │
│ (Phase 1 ✅)    │  │ (Phase 2 ⏳)        │
└──────┬──────────┘  └─┬──────────────────┘
       │              │
┌──────▼──────────┐  ┌─▼──────────────────┐
│ Face Detection  │  │ Speech Metrics     │
│ MediaPipe       │  │ Pitch, Rate, etc   │
└──────┬──────────┘  └─┬──────────────────┘
       │              │
┌──────▼──────────┐  ┌─▼──────────────────┐
│ Expression      │  │ Sentiment Analysis │
│ Recognition     │  │ NLP Models         │
└──────┬──────────┘  └─┬──────────────────┘
       │              │
       └──────┬───────┘
              │
       ┌──────▼─────────────┐
       │ ML Model           │
       │ (Existing Pipeline)│
       └──────┬─────────────┘
              │
    ┌─────────▼──────────┐
    │ Interview Score    │
    │ 0-20 Scale         │
    └────────────────────┘
```

---

## 🚀 Next Steps

### Immediate (This Session)

- ✅ Phase 1 code implemented
- ✅ Dependencies installed
- ⏳ Test real-time dashboard
- ⏳ Verify face detection works

### Phase 2 Preparation (1-3 weeks)

- Speech transcription (Google Speech API)
- Sentiment analysis (transformers)
- Tone/pitch detection
- Speaking rate metrics
- Filler word detection

### Phase 3 Preparation (3-5 weeks)

- Body pose detection (MediaPipe Pose)
- Movement tracking
- Posture analysis
- Hand gesture recognition
- Head position/nod detection

### Phase 4 (5-7 weeks)

- Live dashboard integration
- Real-time combined scoring
- Multi-candidate comparison
- Export to Power BI
- Fine-tune ML model integration

---

## 📚 Code Examples

###Example 1: Process Single Frame

```python
import cv2
from src.real_time_video import InterviewVideoProcessor

processor = InterviewVideoProcessor(source=0)

if processor.video_capture.open():
    success, frame = processor.video_capture.read_frame()

    if success:
        analysis = processor.process_frame(frame)

        print(f"Faces: {analysis['faces_detected']}")
        print(f"Eye Contact: {analysis['eye_contact_score']:.2f}/1.0")
        print(f"Confidence: {analysis['confidence']:.2f}")

        # Show frame with detections
        cv2.imshow("Interview Analysis", analysis['frame_with_overlay'])
        cv2.waitKey(1)
```

### Example 2: Analyze Expressions

```python
from src.real_time_video import InterviewVideoProcessor
from src.facial_analysis import FacialExpressionAnalyzer, EmotionScoreCalculator

processor = InterviewVideoProcessor(source=0)
expr_analyzer = FacialExpressionAnalyzer()

success, frame = processor.video_capture.read_frame()
detections = processor.facial_processor.detect_faces(frame)

if detections['landmarks']:
    expressions = expr_analyzer.detect_expressions(detections['landmarks'][0])
    metrics = expr_analyzer.get_interview_metrics()
    score = EmotionScoreCalculator.calculate_expression_score(metrics)

    print(f"Primary Expression: {expressions['primary_expression']}")
    print(f"Expression Score: {score:.1f}/20")
```

### Example 3: Full Session

```python
from src.real_time_video import InterviewVideoProcessor

processor = InterviewVideoProcessor(source=0)

if not processor.video_capture.open():
    print("Cannot open webcam")
    exit()

frames_processed = 0
max_frames = 300  # 10 seconds at 30 FPS

while frames_processed < max_frames:
    success, frame = processor.video_capture.read_frame()
    if not success:
        break

    analysis = processor.process_frame(frame)
    frames_processed += 1

    if frames_processed % 30 == 0:  # Every second
        stats = processor.get_session_stats()
        print(f"Frames: {frames_processed}, Eye Contact: {stats['avg_eye_contact_score']:.2f}")

processor.release()
print("Session complete!")
```

---

## ✅ Checklist

Before moving to Phase 2, verify:

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `app_realtime.py` runs without errors
- [ ] Webcam access works
- [ ] Face detection triggers on your face
- [ ] Eye contact score updates (smile to see it change)
- [ ] Session statistics display correctly
- [ ] Trends/charts render in dashboard

---

## 📞 Support

**Issues?**

1. Check troubleshooting section above
2. Verify camera permissions in Windows Settings
3. Test imports: `python -c "import cv2; import mediapipe"`
4. Check requirements.txt installed: `pip list | grep -E "(opencv|mediapipe|librosa)"`

---

**Status**: ✅ Phase 1 Complete - Ready for Phase 2 Integration
