"""
Real-time video capture and processing for interview analysis.
Captures video from webcam or video file and provides streaming interface.
"""

import cv2
import numpy as np
import mediapipe as mp
from pathlib import Path
from typing import Tuple, Dict, Optional, Generator
import threading
from collections import deque
from datetime import datetime


class RealTimeVideoCapture:
    """Handles video capture from webcam or file with frame preprocessing."""
    
    def __init__(self, source: int = 0, fps: int = 30, resolution: Tuple[int, int] = (1280, 720)):
        """
        Initialize video capture.
        
        Args:
            source: 0 for webcam, or path to video file
            fps: Frames per second (for webcam default)
            resolution: Target resolution (width, height)
        """
        self.source = source
        self.fps = fps
        self.resolution = resolution
        self.cap = None
        self.is_open = False
        self.frame_count = 0
        self.frame_buffer = deque(maxlen=30)  # Keep last 30 frames
        
    def open(self) -> bool:
        """Open video source."""
        try:
            self.cap = cv2.VideoCapture(self.source)
            if not self.cap.isOpened():
                return False
                
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer lag
            
            self.is_open = True
            return True
        except Exception as e:
            print(f"Error opening video source: {e}")
            return False
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read and preprocess a frame.
        
        Returns:
            (success, frame) - success is True if frame read successfully
        """
        if not self.is_open:
            return False, None
            
        ret, frame = self.cap.read()
        if not ret:
            return False, None
            
        # Mirror for webcam (more natural for user)
        if isinstance(self.source, int):  # Webcam
            frame = cv2.flip(frame, 1)
        
        self.frame_count += 1
        self.frame_buffer.append(frame.copy())
        
        return True, frame
    
    def get_frame_count(self) -> int:
        """Get total frames captured."""
        return self.frame_count
    
    def get_fps(self) -> float:
        """Get actual FPS from video source."""
        if self.cap and self.is_open:
            return self.cap.get(cv2.CAP_PROP_FPS)
        return self.fps
    
    def release(self):
        """Release video source."""
        if self.cap:
            self.cap.release()
        self.is_open = False
        self.frame_count = 0


class FacialDetectionProcessor:
    """Processes frames for real-time facial detection and analysis using OpenCV."""
    
    def __init__(self):
        """Initialize face detection with OpenCV cascade classifier."""
        # Load OpenCV face cascade classifier
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        self.detection_history = deque(maxlen=30)
        
    def detect_faces(self, frame: np.ndarray) -> Dict:
        """
        Detect faces in frame using OpenCV.
        
        Args:
            frame: Input frame (BGR)
            
        Returns:
            Dict with detection results
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = frame.shape[:2]
        
        # Detect faces using cascade classifier
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            maxSize=(400, 400)
        )
        
        detections = {
            'faces_detected': len(faces),
            'face_boxes': [],
            'landmarks': [],
            'confidence_scores': [],
            'frame_with_boxes': frame.copy()
        }
        
        # Process detected faces
        for (x, y, fw, fh) in faces:
            x_min = max(0, x)
            y_min = max(0, y)
            x_max = min(w, x + fw)
            y_max = min(h, y + fh)
            
            detections['face_boxes'].append({
                'x_min': x_min, 'y_min': y_min,
                'x_max': x_max, 'y_max': y_max,
                'width': x_max - x_min, 'height': y_max - y_min
            })
            
            # OpenCV cascade gives high confidence
            detections['confidence_scores'].append(0.9)
            
            # Draw box
            cv2.rectangle(detections['frame_with_boxes'], 
                        (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(detections['frame_with_boxes'],
                      'Face: 0.90',
                      (x_min, y_min - 10),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        self.detection_history.append(detections['faces_detected'])
        
        return detections
    
    def analyze_eye_contact(self, frame: np.ndarray, detections: Dict) -> Dict:
        """
        Analyze eye contact based on face position and gaze direction.
        
        Args:
            frame: Input frame
            detections: Detection results from detect_faces
            
        Returns:
            Eye contact analysis metrics
        """
        h, w = frame.shape[:2]
        
        analysis = {
            'eye_contact_score': 0.0,
            'face_centered': False,
            'looking_at_camera': False,
            'face_position': 'unknown',
            'gaze_direction': 'unknown'
        }
        
        if detections['face_boxes']:
            bbox = detections['face_boxes'][0]
            center_x = (bbox['x_min'] + bbox['x_max']) / 2
            center_y = (bbox['y_min'] + bbox['y_max']) / 2
            
            # Check if face is centered (roughly center 1/3 of frame)
            center_region_x_min = w * 0.25
            center_region_x_max = w * 0.75
            center_region_y_min = h * 0.2
            center_region_y_max = h * 0.8
            
            face_centered = (center_region_x_min < center_x < center_region_x_max and
                           center_region_y_min < center_y < center_region_y_max)
            
            if face_centered:
                analysis['face_centered'] = True
                analysis['eye_contact_score'] = 0.8
                analysis['looking_at_camera'] = True
                analysis['gaze_direction'] = 'forward'
            else:
                # Determine which direction face is turned
                if center_x < w * 0.25:
                    analysis['gaze_direction'] = 'left'
                    analysis['eye_contact_score'] = 0.3
                elif center_x > w * 0.75:
                    analysis['gaze_direction'] = 'right'
                    analysis['eye_contact_score'] = 0.3
                else:
                    analysis['gaze_direction'] = 'center'
                    analysis['eye_contact_score'] = 0.6
                
                if center_y > h * 0.8:
                    analysis['face_position'] = 'looking_down'
                    analysis['eye_contact_score'] *= 0.5
                elif center_y < h * 0.2:
                    analysis['face_position'] = 'looking_up'
                    analysis['eye_contact_score'] *= 0.7
        
        return analysis
    
    def release(self):
        """Clean up resources."""
        self.face_detection.close()
        self.face_mesh.close()


class InterviewVideoProcessor:
    """Combined processor for real-time interview analysis."""
    
    def __init__(self, source: int = 0):
        """Initialize video and facial processors."""
        self.video_capture = RealTimeVideoCapture(source)
        self.facial_processor = FacialDetectionProcessor()
        self.start_time = None
        self.frame_metrics = deque(maxlen=100)
        
    def process_frame(self, frame: np.ndarray) -> Dict:
        """
        Process single frame for interview analysis.
        
        Returns:
            Comprehensive frame analysis
        """
        detections = self.facial_processor.detect_faces(frame)
        eye_contact = self.facial_processor.analyze_eye_contact(frame, detections)
        
        analysis = {
            'timestamp': datetime.now(),
            'faces_detected': detections['faces_detected'],
            'face_boxes': detections['face_boxes'],
            'confidence': max(detections['confidence_scores']) if detections['confidence_scores'] else 0.0,
            'eye_contact_score': eye_contact['eye_contact_score'],
            'looking_at_camera': eye_contact['looking_at_camera'],
            'face_centered': eye_contact['face_centered'],
            'gaze_direction': eye_contact['gaze_direction'],
            'frame_with_overlay': detections['frame_with_boxes']
        }
        
        self.frame_metrics.append(analysis)
        return analysis
    
    def get_session_stats(self) -> Dict:
        """Get statistics for entire session so far."""
        if not self.frame_metrics:
            return {}
        
        metrics = list(self.frame_metrics)
        
        return {
            'total_frames_analyzed': len(metrics),
            'avg_faces_detected': np.mean([m['faces_detected'] for m in metrics]),
            'avg_eye_contact_score': np.mean([m['eye_contact_score'] for m in metrics]),
            'avg_confidence': np.mean([m['confidence'] for m in metrics]),
            'looking_at_camera_pct': (
                sum(1 for m in metrics if m['looking_at_camera']) / len(metrics) * 100
            ) if metrics else 0,
            'face_centered_pct': (
                sum(1 for m in metrics if m['face_centered']) / len(metrics) * 100
            ) if metrics else 0
        }
    
    def release(self):
        """Clean up resources."""
        self.video_capture.release()
        self.facial_processor.release()


def stream_video(source: int = 0, callback=None) -> Generator:
    """
    Stream video frames with analysis.
    
    Args:
        source: Video source (0 for webcam)
        callback: Optional callback function for each frame
        
    Yields:
        Analyzed frame data
    """
    processor = InterviewVideoProcessor(source)
    
    if not processor.video_capture.open():
        print("Failed to open video source")
        return
    
    try:
        while True:
            success, frame = processor.video_capture.read_frame()
            if not success:
                break
            
            analysis = processor.process_frame(frame)
            
            if callback:
                callback(analysis)
            
            yield analysis
            
    finally:
        processor.release()
