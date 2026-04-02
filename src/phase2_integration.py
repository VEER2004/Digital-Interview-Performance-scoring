"""
Phase 2: Real-Time Speech & Audio Analysis Integration
Integrates speech analysis with Phase 1 video for combined metrics.
"""

import numpy as np
import threading
import queue
from typing import Dict, Optional, List, Tuple
from collections import deque, defaultdict
from datetime import datetime
import json
from pathlib import Path
import librosa


class RealTimeTranscriptionProcessor:
    """
    Real-time speech-to-text processor.
    Combines MediaPipe Face detection with speech analysis.
    """
    
    def __init__(self, sample_rate: int = 16000):
        """Initialize transcription processor."""
        self.sample_rate = sample_rate
        self.transcript_buffer = deque(maxlen=1000)  # Keep last 1000 words
        self.sentence_history = deque(maxlen=50)  # Last 50 sentences
        self.is_speaking = False
        self.silence_threshold = 0.02
        self.speech_start_time = None
        
    def detect_speech_segments(self, audio_data: np.ndarray) -> List[Dict]:
        """
        Detect start/stop of speech segments.
        
        Args:
            audio_data: Audio waveform
            
        Returns:
            List of speech segments with timestamps
        """
        # Calculate energy in time windows
        frame_length = 2048
        hop_length = 512
        
        S = librosa.feature.melspectrogram(y=audio_data, sr=self.sample_rate,
                                          n_fft=frame_length, hop_length=hop_length)
        S_db = librosa.power_to_db(S, ref=np.max)
        energy = np.mean(S_db, axis=0)
        
        # Simple threshold-based VAD (Voice Activity Detection)
        threshold = np.mean(energy) + np.std(energy) * 0.5
        speech_frames = energy > threshold
        
        # Find segments (consecutive True values)
        segments = []
        segment_start = None
        
        for i, is_speech in enumerate(speech_frames):
            if is_speech and segment_start is None:
                segment_start = i
            elif not is_speech and segment_start is not None:
                start_time = librosa.frames_to_time(segment_start, sr=self.sample_rate,
                                                    hop_length=hop_length)
                end_time = librosa.frames_to_time(i, sr=self.sample_rate,
                                                 hop_length=hop_length)
                segments.append({
                    'start': start_time,
                    'end': end_time,
                    'duration': end_time - start_time
                })
                segment_start = None
        
        return segments
    
    def analyze_speaking_patterns(self, audio_data: np.ndarray) -> Dict:
        """
        Analyze speaking patterns: pace, pauses, rhythm.
        
        Args:
            audio_data: Audio waveform
            
        Returns:
            Speaking pattern analysis
        """
        segments = self.detect_speech_segments(audio_data)
        
        if not segments:
            return {
                'speech_segments': 0,
                'total_speaking_time': 0,
                'avg_segment_duration': 0,
                'pause_count': 0,
                'avg_pause_duration': 0,
                'speaking_rhythm_score': 0.5
            }
        
        # Calculate metrics
        total_speaking = sum(s['duration'] for s in segments)
        avg_segment = np.mean([s['duration'] for s in segments])
        
        # Pause calculation (gaps between segments)
        pauses = []
        for i in range(len(segments) - 1):
            pause_duration = segments[i+1]['start'] - segments[i]['end']
            if pause_duration > 0.1:  # Only count meaningful pauses
                pauses.append(pause_duration)
        
        # Score: good rhythm is 3-5 second segments with 0.5-1s pauses
        rhythm_score = 0.5
        if avg_segment > 2 and avg_segment < 6:  # Good segment length
            rhythm_score += 0.25
        if pauses and 0.3 < np.mean(pauses) < 1.5:  # Good pause length
            rhythm_score += 0.25
        
        return {
            'speech_segments': len(segments),
            'total_speaking_time': total_speaking,
            'avg_segment_duration': avg_segment,
            'pause_count': len(pauses),
            'avg_pause_duration': np.mean(pauses) if pauses else 0,
            'speaking_rhythm_score': min(1.0, rhythm_score)  # 0-1 scale
        }


class EnhancedSentimentAnalyzer:
    """Enhanced sentiment with context and emotion detection."""
    
    POSITIVE_INDICATORS = {
        'very positive': ['excellent', 'fantastic', 'amazing', 'love', 'great', 'wonderful'],
        'positive': ['good', 'nice', 'happy', 'enjoy', 'appreciate', 'thank'],
        'confident': ['certain', 'definitely', 'absolutely', 'sure', 'obviously']
    }
    
    NEGATIVE_INDICATORS = {
        'very negative': ['terrible', 'awful', 'hate', 'horrible', 'worst', 'disaster'],
        'negative': ['bad', 'wrong', 'poor', 'disappointed', 'problem', 'issue'],
        'uncertain': ['maybe', 'perhaps', 'uncertain', 'doubt', 'unsure']
    }
    
    def __init__(self):
        """Initialize sentiment analyzer."""
        self.sentiment_history = deque(maxlen=100)
        
    def analyze_with_context(self, text: str, previous_context: Optional[str] = None) -> Dict:
        """
        Analyze sentiment with contextual awareness.
        
        Args:
            text: Text to analyze
            previous_context: Previous statement for context
            
        Returns:
            Detailed sentiment analysis
        """
        if not text.strip():
            return self._empty_sentiment()
        
        text_lower = text.lower()
        words = set(text_lower.split())
        
        # Score calculation
        positive_score = 0.0
        negative_score = 0.0
        confidence_score = 0.0
        
        # Check indicators
        for level, indicators in self.POSITIVE_INDICATORS.items():
            for indicator in indicators:
                if indicator in text_lower:
                    if 'very' in level:
                        positive_score += 0.3
                    elif 'confident' in level:
                        confidence_score += 0.2
                    else:
                        positive_score += 0.15
        
        for level, indicators in self.NEGATIVE_INDICATORS.items():
            for indicator in indicators:
                if indicator in text_lower:
                    if 'very' in level:
                        negative_score += 0.3
                    elif 'uncertain' in level:
                        confidence_score -= 0.1
                    else:
                        negative_score += 0.15
        
        # Normalize scores
        total = positive_score + negative_score + abs(confidence_score)
        if total > 0:
            positive_score = min(1.0, positive_score / total * 2)
            negative_score = min(1.0, negative_score / total * 2)
            confidence_score = min(1.0, max(0.0, confidence_score))
        else:
            positive_score = 0.33
            negative_score = 0.33
            confidence_score = 0.34
        
        # Determine sentiment
        if positive_score > 0.6:
            sentiment = 'positive'
        elif negative_score > 0.6:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        result = {
            'sentiment': sentiment,
            'positive_score': positive_score,
            'negative_score': negative_score,
            'confidence_score': confidence_score,
            'emotion_type': self._classify_emotion(text_lower),
            'intensity': min(1.0, positive_score + negative_score)
        }
        
        self.sentiment_history.append(result)
        return result
    
    def _empty_sentiment(self) -> Dict:
        """Return neutral sentiment."""
        return {
            'sentiment': 'neutral',
            'positive_score': 0.33,
            'negative_score': 0.33,
            'confidence_score': 0.34,
            'emotion_type': 'neutral',
            'intensity': 0.0
        }
    
    def _classify_emotion(self, text: str) -> str:
        """Classify specific emotion from text."""
        emotions = {
            'excited': ['excited', 'thrilled', 'amazing', 'fantastic'],
            'confident': ['confident', 'sure', 'certain', 'absolutely'],
            'uncertain': ['uncertain', 'unsure', 'maybe', 'perhaps'],
            'frustrated': ['frustrated', 'annoyed', 'irritated', 'angry'],
            'sad': ['sad', 'disappointed', 'down', 'depressed'],
            'neutral': []
        }
        
        for emotion, keywords in emotions.items():
            if any(kw in text for kw in keywords):
                return emotion
        
        return 'neutral'
    
    def get_sentiment_trend(self) -> Dict:
        """Get trending sentiment across session."""
        if not self.sentiment_history:
            return {}
        
        sentiments = list(self.sentiment_history)
        positive_avg = np.mean([s['positive_score'] for s in sentiments])
        negative_avg = np.mean([s['negative_score'] for s in sentiments])
        confidence_avg = np.mean([s['confidence_score'] for s in sentiments])
        
        return {
            'trend_positive': positive_avg,
            'trend_negative': negative_avg,
            'trend_confidence': confidence_avg,
            'overall_sentiment': 'positive' if positive_avg > negative_avg else 'negative' if negative_avg > positive_avg else 'neutral',
            'total_statements': len(sentiments)
        }


class Phase2SpeechMetricsCalculator:
    """Calculate comprehensive speech quality metrics."""
    
    @staticmethod
    def calculate_speech_confidence_score(
        transcription: str,
        speaking_rate: float,
        pitch_variance: float,
        sentiment: Dict
    ) -> float:
        """
        Calculate speech confidence score (0-20).
        
        Args:
            transcription: Transcribed text
            speaking_rate: Words per minute
            pitch_variance: Pitch variation (0-1)
            sentiment: Sentiment analysis result
            
        Returns:
            Speech quality score 0-20
        """
        score = 10.0  # Base score
        
        # Speaking rate component (ideal: 120-150 WPM)
        if 100 < speaking_rate < 160:
            rate_contrib = 3
        elif 80 < speaking_rate < 180:
            rate_contrib = 2
        else:
            rate_contrib = 0
        
        # Pitch variance (higher variety = better)
        variance_contrib = pitch_variance * 4  # 0-4 points
        
        # Sentiment confidence (confident speakers score higher)
        sentiment_contrib = sentiment.get('confidence_score', 0.5) * 3  # 0-3 points
        
        # Text clarity (fewer filler words = better)
        filler_words = {'um', 'uh', 'like', 'you know', 'basically', 'literally'}
        text_lower = transcription.lower()
        filler_count = sum(1 for f in filler_words if f in text_lower)
        clarity_contrib = max(0, 3 - filler_count * 0.5)  # 0-3 points
        
        # Text length (longer responses = more complete)
        word_count = len(transcription.split())
        length_contrib = min(2, word_count / 50)  # 0-2 points
        
        score += rate_contrib + variance_contrib + sentiment_contrib + clarity_contrib + length_contrib
        
        return max(0.0, min(20.0, score))


class Phase2IntegratedAnalysis:
    """
    Combines Phase 1 (Video) + Phase 2 (Speech) for integrated metrics.
    """
    
    def __init__(self):
        """Initialize integrated analyzer."""
        self.transcription_processor = RealTimeTranscriptionProcessor()
        self.sentiment_analyzer = EnhancedSentimentAnalyzer()
        self.metrics_calculator = Phase2SpeechMetricsCalculator()
        self.session_data = deque(maxlen=1000)
        
    def combine_video_audio_metrics(
        self,
        video_metrics: Dict,
        audio_metrics: Dict,
        transcription: str,
        sentiment: Dict
    ) -> Dict:
        """
        Combine video and audio metrics into unified analysis.
        
        Args:
            video_metrics: From Phase 1 (facial, eye contact, expressions)
            audio_metrics: From Phase 2 (speech rate, pitch, energy)
            transcription: Speech transcription
            sentiment: Sentiment analysis
            
        Returns:
            Integrated metrics combining both
        """
        # Extract key components
        eye_contact_score = video_metrics.get('eye_contact_score', 0.5)
        facial_engagement = video_metrics.get('facial_engagement_score', 10.0)
        
        speaking_rate = audio_metrics.get('speech_metrics', {}).get('words_per_minute', 120)
        pitch_variance = audio_metrics.get('speech_metrics', {}).get('pitch_variance', 0.5)
        energy = audio_metrics.get('speech_metrics', {}).get('rms_energy', 0.5)
        
        # Calculate speech confidence
        speech_confidence = self.metrics_calculator.calculate_speech_confidence_score(
            transcription, speaking_rate, pitch_variance, sentiment
        )
        
        # Calculate engagement composite (0-20)
        # Weights: 30% facial, 30% speech, 20% sentiment, 20% energy/pace
        composite_engagement = (
            (facial_engagement * 0.3) +
            (speech_confidence * 0.3) +
            (sentiment.get('intensity', 0.5) * 20 * 0.2) +
            ((energy / 0.5) * 10 * 0.2)  # Normalize energy
        )
        
        # Cap at 20
        composite_engagement = min(20.0, composite_engagement)
        
        result = {
            'timestamp': datetime.now(),
            'video_metrics': video_metrics,
            'audio_metrics': audio_metrics,
            'transcription': transcription,
            'sentiment': sentiment,
            'speech_confidence': speech_confidence,
            'composite_engagement_score': composite_engagement,
            'components': {
                'facial_component': facial_engagement,
                'speech_component': speech_confidence,
                'sentiment_component': sentiment.get('intensity', 0.5) * 20,
                'energy_component': (energy / 0.5) * 10
            }
        }
        
        self.session_data.append(result)
        return result
    
    def get_session_analysis_summary(self) -> Dict:
        """Get comprehensive session analysis."""
        if not self.session_data:
            return {}
        
        data_list = list(self.session_data)
        
        return {
            'total_frames': len(data_list),
            'avg_engagement_score': np.mean([d['composite_engagement_score'] for d in data_list]),
            'avg_facial_score': np.mean([d['components']['facial_component'] for d in data_list]),
            'avg_speech_score': np.mean([d['components']['speech_component'] for d in data_list]),
            'sentiment_trend': self.sentiment_analyzer.get_sentiment_trend(),
            'speaking_patterns': self._analyze_speaking_patterns(data_list),
            'overall_performance': self._calculate_overall_performance(data_list)
        }
    
    def _analyze_speaking_patterns(self, data_list: List[Dict]) -> Dict:
        """Analyze speaking patterns across session."""
        speech_scores = [d['components']['speech_component'] for d in data_list]
        
        return {
            'consistency': float(1.0 - (np.std(speech_scores) / (np.mean(speech_scores) + 0.001))),
            'improvement_trend': self._calculate_trend(speech_scores),
            'peak_performance': float(max(speech_scores)),
            'valley_performance': float(min(speech_scores))
        }
    
    def _calculate_trend(self, scores: List[float]) -> str:
        """Determine if performance is improving, stable, or declining."""
        if len(scores) < 2:
            return 'insufficient_data'
        
        first_half = np.mean(scores[:len(scores)//2])
        second_half = np.mean(scores[len(scores)//2:])
        
        diff = second_half - first_half
        if diff > 1:
            return 'improving'
        elif diff < -1:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_overall_performance(self, data_list: List[Dict]) -> Dict:
        """Calculate overall performance rating."""
        if not data_list:
            return {}
        
        avg_score = np.mean([d['composite_engagement_score'] for d in data_list])
        
        if avg_score >= 16:
            rating = 'Excellent'
            feedback = 'Outstanding interview performance'
        elif avg_score >= 13:
            rating = 'Good'
            feedback = 'Above average performance'
        elif avg_score >= 10:
            rating = 'Average'
            feedback = 'Meet expectations'
        else:
            rating = 'Needs Improvement'
            feedback = 'Below expectations'
        
        return {
            'overall_score': avg_score,
            'rating': rating,
            'feedback': feedback,
            'strengths': self._identify_strengths(data_list),
            'areas_for_improvement': self._identify_weaknesses(data_list)
        }
    
    def _identify_strengths(self, data_list: List[Dict]) -> List[str]:
        """Identify interview strengths."""
        strengths = []
        
        avg_facial = np.mean([d['components']['facial_component'] for d in data_list])
        avg_speech = np.mean([d['components']['speech_component'] for d in data_list])
        
        if avg_facial > 14:
            strengths.append('Strong facial expressions and engagement')
        if avg_speech > 14:
            strengths.append('Clear and confident speaking')
        
        sentiment_trend = self.sentiment_analyzer.get_sentiment_trend()
        if sentiment_trend.get('trend_confidence', 0) > 0.6:
            strengths.append('High confidence throughout')
        
        return strengths if strengths else ['Consistent performance']
    
    def _identify_weaknesses(self, data_list: List[Dict]) -> List[str]:
        """Identify areas for improvement."""
        weaknesses = []
        
        avg_facial = np.mean([d['components']['facial_component'] for d in data_list])
        avg_speech = np.mean([d['components']['speech_component'] for d in data_list])
        
        if avg_facial < 12:
            weaknesses.append('Could improve facial expressions and eye contact')
        if avg_speech < 12:
            weaknesses.append('Speaking pace or clarity needs improvement')
        
        sentiment_trend = self.sentiment_analyzer.get_sentiment_trend()
        if sentiment_trend.get('trend_confidence', 0) < 0.4:
            weaknesses.append('Consider speaking with more conviction')
        
        return weaknesses if weaknesses else []
