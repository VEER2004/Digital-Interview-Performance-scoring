"""
Facial expression and emotion analysis using deep learning.
Detects expressions, emotions, and provides expression-based interview metrics.
"""

import numpy as np
from typing import Dict, List, Tuple
import cv2
from collections import deque, defaultdict
from datetime import datetime


class FacialExpressionAnalyzer:
    """Analyzes facial expressions for interview context."""
    
    # Expression confidence thresholds
    EXPRESSION_THRESHOLDS = {
        'smile': 0.5,
        'neutral': 0.6,
        'frown': 0.5,
        'surprise': 0.4,
        'anger': 0.4,
        'disgust': 0.4,
        'fear': 0.4,
        'sad': 0.5
    }
    
    # Emotion categories for interview scoring
    POSITIVE_EXPRESSIONS = ['smile', 'surprise']
    NEGATIVE_EXPRESSIONS = ['frown', 'anger', 'disgust', 'fear', 'sad']
    NEUTRAL_EXPRESSIONS = ['neutral']
    
    def __init__(self, history_size: int = 100):
        """Initialize expression analyzer."""
        self.history_size = history_size
        self.expression_history = deque(maxlen=history_size)
        self.emotion_counts = defaultdict(int)
        self.total_frames = 0
        
    def detect_expressions(self, landmarks: List[Dict]) -> Dict:
        """
        Calculate facial expressions from landmarks.
        
        Args:
            landmarks: List of facial landmarks from MediaPipe
            
        Returns:
            Expression confidence scores and primary expression
        """
        expressions = {
            'smile': 0.0,
            'neutral': 0.0,
            'frown': 0.0,
            'surprise': 0.0,
            'anger': 0.0,
            'disgust': 0.0,
            'fear': 0.0,
            'sad': 0.0,
            'primary_expression': 'unknown'
        }
        
        if not landmarks or len(landmarks) < 468:  # MediaPipe has 468 points
            return expressions
        
        try:
            # Eye coordinates
            left_eye = self._get_eye_region(landmarks, 'left')
            right_eye = self._get_eye_region(landmarks, 'right')
            
            # Mouth coordinates
            mouth_top = self._get_point(landmarks, 13)  # Upper lip
            mouth_bottom = self._get_point(landmarks, 14)  # Lower lip
            mouth_left = self._get_point(landmarks, 78)  # Left mouth corner
            mouth_right = self._get_point(landmarks, 308)  # Right mouth corner
            
            # Eyebrow coordinates
            left_brow = self._get_point(landmarks, 46)  # Left eyebrow
            right_brow = self._get_point(landmarks, 276)  # Right eyebrow
            
            # Calculate distances
            mouth_height = abs(mouth_bottom['y'] - mouth_top['y'])
            mouth_width = abs(mouth_right['x'] - mouth_left['x'])
            eye_openness = (left_eye['openness'] + right_eye['openness']) / 2
            eyebrow_height = abs(left_brow['y'] - right_brow['y'])
            
            # Determine expressions
            mouth_ratio = mouth_height / (mouth_width + 0.001)
            
            # Smile detection
            if mouth_height > 0.02 and mouth_ratio > 0.15:
                expressions['smile'] = min(0.9, mouth_height / 0.04)
            
            # Frown detection
            if mouth_height > 0.01 and mouth_ratio < 0.08:
                expressions['frown'] = min(0.8, (0.02 - mouth_height) / 0.01)
            
            # Neutral detection
            if 0.01 < mouth_height < 0.03 and 0.1 < mouth_ratio < 0.2:
                expressions['neutral'] = 0.7 + (eye_openness * 0.3)
            
            # Surprise detection (high eye openness, mouth open)
            if eye_openness > 0.7 and mouth_height > 0.025:
                expressions['surprise'] = min(0.9, (eye_openness + mouth_height / 0.05) / 2)
            
            # Anger detection (lowered eyebrows, narrowed eyes)
            if eye_openness < 0.5 and eyebrow_height < 0.02:
                expressions['anger'] = 0.6 + (0.5 - eye_openness) * 0.4
            
            # Fear detection (high eyebrows, wide eyes)
            if eyebrow_height > 0.04 and eye_openness > 0.6:
                expressions['fear'] = min(0.7, (eyebrow_height / 0.05 + eye_openness) / 2)
            
            # Disgust detection (nose wrinkle effect from landmarks)
            expressions['disgust'] = 0.2 if mouth_height < 0.015 else 0.1
            
            # Sad detection (downturned mouth, lowered eyebrows)
            if mouth_ratio < 0.08 and eyebrow_height < 0.02:
                expressions['sad'] = 0.6
            
            # Normalize to max 1.0
            for expr in expressions:
                if expr != 'primary_expression':
                    expressions[expr] = min(1.0, max(0.0, expressions[expr]))
            
            # Determine primary expression
            max_expr = max(
                ((k, v) for k, v in expressions.items() if k != 'primary_expression'),
                key=lambda x: x[1]
            )
            
            if max_expr[1] > 0.3:
                expressions['primary_expression'] = max_expr[0]
                
        except (IndexError, KeyError):
            pass
        
        self.expression_history.append(expressions.copy())
        self.emotion_counts[expressions['primary_expression']] += 1
        self.total_frames += 1
        
        return expressions
    
    def _get_eye_region(self, landmarks: List[Dict], side: str) -> Dict:
        """Calculate eye region metrics."""
        if side == 'left':
            top = self._get_point(landmarks, 159)
            bottom = self._get_point(landmarks, 145)
            left = self._get_point(landmarks, 133)
            right = self._get_point(landmarks, 155)
        else:  # right
            top = self._get_point(landmarks, 386)
            bottom = self._get_point(landmarks, 374)
            left = self._get_point(landmarks, 263)
            right = self._get_point(landmarks, 362)
        
        vertical_dist = abs(bottom['y'] - top['y'])
        horizontal_dist = abs(right['x'] - left['x'])
        
        return {
            'openness': vertical_dist / (horizontal_dist + 0.001),
            'vertical_dist': vertical_dist,
            'horizontal_dist': horizontal_dist
        }
    
    def _get_point(self, landmarks: List[Dict], index: int) -> Dict:
        """Safe point retrieval."""
        if index < len(landmarks):
            return landmarks[index]
        return {'x': 0, 'y': 0, 'z': 0}
    
    def get_interview_metrics(self) -> Dict:
        """
        Calculate interview performance metrics based on expressions.
        
        Returns:
            Metrics for interview scoring
        """
        if not self.expression_history:
            return {}
        
        expressions = list(self.expression_history)
        
        metrics = {
            'avg_smile_score': np.mean([e['smile'] for e in expressions]),
            'avg_neutral_score': np.mean([e['neutral'] for e in expressions]),
            'smile_frequency': sum(1 for e in expressions if e['primary_expression'] == 'smile') / len(expressions),
            'frown_frequency': sum(1 for e in expressions if e['primary_expression'] == 'frown') / len(expressions),
            'positive_expression_pct': sum(
                1 for e in expressions if e['primary_expression'] in self.POSITIVE_EXPRESSIONS
            ) / len(expressions) * 100,
            'negative_expression_pct': sum(
                1 for e in expressions if e['primary_expression'] in self.NEGATIVE_EXPRESSIONS
            ) / len(expressions) * 100,
            'neutral_expression_pct': sum(
                1 for e in expressions if e['primary_expression'] in self.NEUTRAL_EXPRESSIONS
            ) / len(expressions) * 100,
            'emotion_distribution': dict(self.emotion_counts),
            'total_frames_analyzed': self.total_frames
        }
        
        return metrics
    
    def reset(self):
        """Reset analysis state."""
        self.expression_history.clear()
        self.emotion_counts.clear()
        self.total_frames = 0


class EmotionScoreCalculator:
    """Converts emotion metrics to interview performance scores (0-20)."""
    
    @staticmethod
    def calculate_expression_score(metrics: Dict) -> float:
        """
        Convert expression metrics to 0-20 score.
        
        Args:
            metrics: Expression metrics from FacialExpressionAnalyzer
            
        Returns:
            Score 0-20 (higher is better)
        """
        if not metrics:
            return 10.0  # Default middle score
        
        score = 10.0  # Base score
        
        # Positive expressions increase score
        smile_contrib = metrics.get('smile_frequency', 0) * 5
        positive_pct = metrics.get('positive_expression_pct', 0)
        positive_contrib = (positive_pct / 100) * 5
        
        # Negative expressions decrease score
        negative_pct = metrics.get('negative_expression_pct', 0)
        negative_contrib = (negative_pct / 100) * -3
        
        # Neutral is baseline
        neutral_pct = metrics.get('neutral_expression_pct', 0)
        
        # Calculate final score
        score += smile_contrib
        score += positive_contrib
        score += negative_contrib
        
        # Bonus for balanced expression (some variation is good)
        emotion_dist = metrics.get('emotion_distribution', {})
        if len(emotion_dist) > 1:
            score += 1  # Slight bonus for variety
        
        # Clamp to 0-20 range
        return max(0.0, min(20.0, score))
    
    @staticmethod
    def calculate_engagement_score(eye_contact_score: float, expression_metrics: Dict) -> float:
        """
        Calculate engagement score combining eye contact and expressions (0-20).
        
        Args:
            eye_contact_score: Score from facial detection (0-1)
            expression_metrics: Emotion metrics
            
        Returns:
            Score 0-20
        """
        score = 10.0
        
        # Eye contact component (40% weight)
        eye_contact_contrib = eye_contact_score * 8
        
        # Expression component (20% weight)
        expression_score = EmotionScoreCalculator.calculate_expression_score(expression_metrics)
        expression_contrib = (expression_score / 20) * 4
        
        # Smile prevalence (20% weight)
        smile_freq = expression_metrics.get('smile_frequency', 0)
        smile_contrib = smile_freq * 4
        
        # Engagement bonus for positive expressions (20% weight)
        positive_pct = expression_metrics.get('positive_expression_pct', 0)
        positive_contrib = (positive_pct / 100) * 4
        
        score = eye_contact_contrib + expression_contrib + smile_contrib + positive_contrib
        
        return max(0.0, min(20.0, score))
