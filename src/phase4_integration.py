"""
Phase 4: Complete Integration & Unified Interview Scoring
Combines Phases 1-3 (Video, Speech, Body) into single interview score.
Integrates with ML model and Power BI.
"""

import numpy as np
import pandas as pd
import joblib
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import json
from collections import deque
import logging


class UnifiedInterviewScorer:
    """
    Calculates unified interview score combining all phases.
    
    Score Breakdown:
    - 30%: Facial Analysis (expressions, eye contact, engagement)
    - 25%: Speech Analysis (clarity, pace, confidence)
    - 20%: Body Language (posture, gestures, movement)
    - 15%: Consistency & Trend (improvement, stability)
    - 10%: Integration Bonus (how well components work together)
    """
    
    # Weighting coefficients
    WEIGHTS = {
        'facial': 0.30,
        'speech': 0.25,
        'body': 0.20,
        'consistency': 0.15,
        'integration': 0.10
    }
    
    def __init__(self, ml_model_path: Optional[str] = None):
        """
        Initialize unified scorer.
        
        Args:
            ml_model_path: Path to trained ML model (optional)
        """
        self.ml_model = None
        self.metric_history = deque(maxlen=1000)
        self.logger = self._setup_logger()
        
        if ml_model_path and Path(ml_model_path).exists():
            try:
                self.ml_model = joblib.load(ml_model_path)
                self.logger.info(f"Loaded ML model from {ml_model_path}")
            except Exception as e:
                self.logger.warning(f"Could not load ML model: {e}")
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for tracking."""
        logger = logging.getLogger('UnifiedInterviewScorer')
        if not logger.handlers:
            handler = logging.StreamHandler()
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
    
    def calculate_unified_score(
        self,
        facial_metrics: Dict,
        speech_metrics: Dict,
        body_metrics: Dict,
        composite_engagement: Optional[float] = None
    ) -> Dict:
        """
        Calculate unified interview score (0-20).
        
        Args:
            facial_metrics: From Phase 1 (eye contact, expressions, engagement)
            speech_metrics: From Phase 2 (confidence, clarity, sentiment)
            body_metrics: From Phase 3 (posture, gestures, movement)
            composite_engagement: Combined engagement score if available
            
        Returns:
            Complete scoring breakdown
        """
        # Extract component scores (normalized to 0-20)
        facial_score = self._normalize_score(
            facial_metrics.get('engagement_score', 10.0)
        )
        
        speech_score = self._normalize_score(
            speech_metrics.get('speech_confidence', 10.0)
        )
        
        body_score = self._normalize_score(
            body_metrics.get('body_language_score', 10.0)
        )
        
        # Calculate consistency and trend bonus
        consistency_bonus = self._calculate_consistency_bonus()
        
        # Calculate integration bonus (synergy between components)
        integration_bonus = self._calculate_integration_bonus(
            facial_score, speech_score, body_score
        )
        
        # Weighted calculation
        unified_score = (
            facial_score * self.WEIGHTS['facial'] +
            speech_score * self.WEIGHTS['speech'] +
            body_score * self.WEIGHTS['body'] +
            consistency_bonus * self.WEIGHTS['consistency'] +
            integration_bonus * self.WEIGHTS['integration']
        )
        
        # Cap at 20
        unified_score = min(20.0, unified_score)
        
        result = {
            'unified_interview_score': unified_score,
            'timestamp': datetime.now(),
            'component_scores': {
                'facial': facial_score,
                'speech': speech_score,
                'body': body_score,
                'consistency': consistency_bonus,
                'integration': integration_bonus
            },
            'score_breakdown': {
                'facial_contribution': facial_score * self.WEIGHTS['facial'],
                'speech_contribution': speech_score * self.WEIGHTS['speech'],
                'body_contribution': body_score * self.WEIGHTS['body'],
                'consistency_contribution': consistency_bonus * self.WEIGHTS['consistency'],
                'integration_contribution': integration_bonus * self.WEIGHTS['integration']
            },
            'performance_level': self._classify_performance(unified_score),
            'recommendation': self._generate_recommendation(unified_score, facial_metrics, speech_metrics, body_metrics)
        }
        
        self.metric_history.append(result)
        return result
    
    def _normalize_score(self, score: float) -> float:
        """Normalize score to 0-20 range."""
        return max(0.0, min(20.0, float(score)))
    
    def _calculate_consistency_bonus(self) -> float:
        """
        Calculate consistency bonus based on historical data (0-20).
        Higher consistency = higher bonus.
        """
        if len(self.metric_history) < 2:
            return 10.0  # Neutral score
        
        recent_scores = [
            m['unified_interview_score']
            for m in list(self.metric_history)[-10:]  # Last 10 records
        ]
        
        # Low variance = high consistency = high bonus
        variance = np.std(recent_scores) if len(recent_scores) > 1 else 0
        consistency = 1.0 if variance == 0 else 1.0 / (1 + variance)
        
        # Scale to 0-20
        bonus = consistency * 20
        
        # Check for improvement trend
        if len(recent_scores) >= 3:
            first_third = np.mean(recent_scores[:len(recent_scores)//3])
            last_third = np.mean(recent_scores[-len(recent_scores)//3:])
            
            if last_third > first_third + 1:  # Clear improvement
                bonus += 2
        
        return min(20.0, bonus)
    
    def _calculate_integration_bonus(
        self,
        facial_score: float,
        speech_score: float,
        body_score: float
    ) -> float:
        """
        Calculate integration bonus for how well components work together.
        
        Theory: Great interviews have harmony between all components.
        If speech is strong but body is weak = less bonus.
        """
        # Calculate synergy (all components should be similar level)
        scores = np.array([facial_score, speech_score, body_score])
        mean_score = np.mean(scores)
        variance = np.std(scores)
        
        # Low variance between components = good synergy
        synergy = 1.0 if variance == 0 else 1.0 / (1 + variance / 10)
        
        # Base bonus
        bonus = 10.0 + (synergy * 10)
        
        # Bonus if all components are strong
        if all(s > 15 for s in scores):
            bonus += 2
        
        # Bonus if no component is weak (< 8)
        if all(s > 8 for s in scores):
            bonus += 1
        
        return min(20.0, bonus)
    
    def _classify_performance(self, score: float) -> str:
        """Classify performance level."""
        if score >= 18:
            return "Outstanding"
        elif score >= 15:
            return "Excellent"
        elif score >= 12:
            return "Good"
        elif score >= 9:
            return "Average"
        else:
            return "Below Average"
    
    def _generate_recommendation(
        self,
        score: float,
        facial_metrics: Dict,
        speech_metrics: Dict,
        body_metrics: Dict
    ) -> str:
        """Generate actionable recommendation."""
        recommendations = []
        
        # Facial analysis
        facial_score = facial_metrics.get('engagement_score', 10.0)
        if facial_score < 10:
            recommendations.append("Improve eye contact and facial expressions")
        
        # Speech analysis
        speech_score = speech_metrics.get('speech_confidence', 10.0)
        if speech_score < 10:
            recommendations.append("Speak more clearly and confidently")
        
        # Body language
        body_score = body_metrics.get('body_language_score', 10.0)
        if body_score < 10:
            recommendations.append("Improve posture and body awareness")
        
        # Overall
        if score < 12 and recommendations:
            return "; ".join(recommendations)
        elif score >= 15:
            return "Excellent performance - maintain current approach"
        else:
            return "Good performance - minor improvements possible"
    
    def get_ml_prediction(
        self,
        all_metrics: Dict,
        feature_names: Optional[List[str]] = None
    ) -> Optional[Tuple[float, Dict]]:
        """
        Use trained ML model to predict performance if available.
        
        Args:
            all_metrics: All collected metrics
            feature_names: Expected feature names from model
            
        Returns:
            (prediction, confidence_info) or None
        """
        if not self.ml_model or feature_names is None:
            return None
        
        try:
            # Construct feature vector
            features = []
            for feature_name in feature_names:
                # Map phase 4 metrics to original feature names
                value = self._extract_feature_value(all_metrics, feature_name)
                features.append(value)
            
            # Predict
            prediction = self.ml_model.predict([features])[0]
            
            return {
                'model_prediction': prediction,
                'confidence': 0.9,  # Would need model calibration for real confidence
                'model_features_used': len(feature_names),
                'source': 'Unified Real-time System'
            }
        except Exception as e:
            self.logger.warning(f"ML prediction failed: {e}")
            return None
    
    def _extract_feature_value(self, all_metrics: Dict, feature_name: str) -> float:
        """Extract feature value from unified metrics."""
        feature_map = {
            'eye_contact': lambda m: m.get('facial_metrics', {}).get('eye_contact_score', 0.5) * 20,
            'facial_engagement': lambda m: m.get('facial_metrics', {}).get('engagement_score', 10.0),
            'speech_confidence': lambda m: m.get('speech_metrics', {}).get('speech_confidence', 10.0),
            'body_language': lambda m: m.get('body_metrics', {}).get('body_language_score', 10.0),
            # Add more mappings as needed
        }
        
        if feature_name in feature_map:
            return feature_map[feature_name](all_metrics)
        
        return 0.0


class RealTimeInterviewAnalyzer:
    """Main analyzer combining all phases for real-time interview analysis."""
    
    def __init__(self, ml_model_path: Optional[str] = None):
        """Initialize the complete analyzer."""
        self.unified_scorer = UnifiedInterviewScorer(ml_model_path)
        self.session_data = deque(maxlen=1000)
        self.session_start = datetime.now()
        
    def analyze_frame_complete(
        self,
        video_metrics: Dict,
        speech_metrics: Dict,
        body_metrics: Dict,
        audio_frame_index: Optional[int] = None
    ) -> Dict:
        """
        Complete frame analysis using all phases.
        
        Args:
            video_metrics: Phase 1 (facial detection)
            speech_metrics: Phase 2 (speech analysis)
            body_metrics: Phase 3 (body language)
            audio_frame_index: Optional audio frame index for sync
            
        Returns:
            Complete analysis with unified score
        """
        # Calculate unified score
        unified_result = self.unified_scorer.calculate_unified_score(
            facial_metrics=video_metrics,
            speech_metrics=speech_metrics,
            body_metrics=body_metrics
        )
        
        # Combine all data
        frame_analysis = {
            'frame_index': len(self.session_data),
            'timestamp': datetime.now(),
            'video_metrics': video_metrics,
            'speech_metrics': speech_metrics,
            'body_metrics': body_metrics,
            'unified_score': unified_result['unified_interview_score'],
            'performance_level': unified_result['performance_level'],
            'component_breakdown': unified_result['component_scores'],
            'recommendation': unified_result['recommendation']
        }
        
        self.session_data.append(frame_analysis)
        return frame_analysis
    
    def get_interview_report(self) -> Dict:
        """Generate comprehensive interview report."""
        if not self.session_data:
            return {}
        
        session_list = list(self.session_data)
        
        # Calculate summary statistics
        unified_scores = [d['unified_score'] for d in session_list]
        
        report = {
            'session_duration': (datetime.now() - self.session_start).total_seconds(),
            'total_frames_analyzed': len(session_list),
            'final_interview_score': float(np.mean(unified_scores)),
            'score_trend': self._calculate_trend(unified_scores),
            'performance_level': self.unified_scorer._classify_performance(
                float(np.mean(unified_scores))
            ),
            'component_averages': self._calculate_component_averages(session_list),
            'peak_performance': float(max(unified_scores)),
            'minimum_performance': float(min(unified_scores)),
            'performance_consistency': float(
                1.0 - (np.std(unified_scores) / (np.mean(unified_scores) + 0.001))
            ),
            'strengths': self._identify_strengths(session_list),
            'areas_for_improvement': self._identify_improvements(session_list),
            'detailed_recommendations': self._generate_detailed_recommendations(session_list)
        }
        
        return report
    
    def _calculate_trend(self, scores: List[float]) -> str:
        """Determine score trend."""
        if len(scores) < 3:
            return 'insufficient_data'
        
        first_third = np.mean(scores[:len(scores)//3])
        second_third = np.mean(scores[len(scores)//3:2*len(scores)//3])
        last_third = np.mean(scores[2*len(scores)//3:])
        
        trend_first_to_last = last_third - first_third
        
        if trend_first_to_last > 2:
            return 'strong_improvement'
        elif trend_first_to_last > 0.5:
            return 'slight_improvement'
        elif trend_first_to_last < -2:
            return 'declining'
        elif trend_first_to_last < -0.5:
            return 'slight_decline'
        else:
            return 'stable'
    
    def _calculate_component_averages(self, session_list: List[Dict]) -> Dict:
        """Average scores for each component."""
        components = {}
        
        for comp_name in ['facial', 'speech', 'body', 'consistency', 'integration']:
            scores = [
                d['component_breakdown'].get(comp_name, 10.0)
                for d in session_list
            ]
            components[comp_name] = float(np.mean(scores))
        
        return components
    
    def _identify_strengths(self, session_list: List[Dict]) -> List[str]:
        """Identify interview strengths."""
        strengths = []
        avg_components = self._calculate_component_averages(session_list)
        
        if avg_components.get('facial', 0) > 14:
            strengths.append('Excellent facial expressions and eye contact')
        
        if avg_components.get('speech', 0) > 14:
            strengths.append('Clear, confident speaking')
        
        if avg_components.get('body', 0) > 14:
            strengths.append('Excellent posture and body language')
        
        if avg_components.get('consistency', 0) > 15:
            strengths.append('Very consistent performance throughout')
        
        if not strengths:
            strengths.append('Solid overall performance')
        
        return strengths
    
    def _identify_improvements(self, session_list: List[Dict]) -> List[str]:
        """Identify areas for improvement."""
        improvements = []
        avg_components = self._calculate_component_averages(session_list)
        
        if avg_components.get('facial', 10) < 12:
            improvements.append('Work on maintaining eye contact')
        
        if avg_components.get('speech', 10) < 12:
            improvements.append('Practice speaking more clearly')
        
        if avg_components.get('body', 10) < 12:
            improvements.append('Improve posture awareness')
        
        if not improvements:
            improvements.append('Continue current approach')
        
        return improvements
    
    def _generate_detailed_recommendations(self, session_list: List[Dict]) -> Dict:
        """Generate detailed, actionable recommendations."""
        recommendations = {
            'immediate': [],
            'short_term': [],
            'long_term': []
        }
        
        avg_components = self._calculate_component_averages(session_list)
        avg_score = np.mean([d['unified_score'] for d in session_list])
        
        # Immediate actions
        if avg_components['facial'] < 10:
            recommendations['immediate'].append('Focus on eye contact during next answer')
        
        if avg_components['speech'] < 10:
            recommendations['immediate'].append('Slow down speech and articulate clearly')
        
        # Short term (next week)
        if avg_score < 12:
            recommendations['short_term'].append('Practice mock interviews with recording')
            recommendations['short_term'].append('Get feedback from colleague on body language')
        
        # Long term
        recommendations['long_term'].append('Record and review your own interviews monthly')
        recommendations['long_term'].append('Attend professional communication training')
        
        return recommendations
    
    def export_to_powerbi(self, output_path: str) -> bool:
        """
        Export session data to format suitable for Power BI.
        
        Args:
            output_path: CSV file path for export
            
        Returns:
            Success status
        """
        try:
            session_list = list(self.session_data)
            
            # Flatten data for CSV
            export_data = []
            for record in session_list:
                row = {
                    'timestamp': record['timestamp'],
                    'frame_index': record['frame_index'],
                    'unified_score': record['unified_score'],
                    'performance_level': record['performance_level'],
                    'facial_score': record['component_breakdown'].get('facial', 0),
                    'speech_score': record['component_breakdown'].get('speech', 0),
                    'body_score': record['component_breakdown'].get('body', 0),
                    'eye_contact': record['video_metrics'].get('eye_contact_score', 0),
                    'speech_confidence': record['speech_metrics'].get('speech_confidence', 0),
                    'body_language': record['body_metrics'].get('body_language_score', 0)
                }
                export_data.append(row)
            
            df = pd.DataFrame(export_data)
            df.to_csv(output_path, index=False)
            
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False
