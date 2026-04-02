"""
Real-time speech and audio analysis for interview evaluation.
Captures audio, performs speech-to-text, sentiment analysis, and tone detection.
"""

import numpy as np
import threading
import queue
from typing import Dict, Optional, List, Tuple
from collections import deque, defaultdict
from datetime import datetime
import librosa
import sounddevice as sd
import soundfile as sf
from pathlib import Path
import json


class RealTimeAudioCapture:
    """Captures audio in real-time from microphone or audio file."""
    
    def __init__(self, sample_rate: int = 16000, channels: int = 1, chunk_size: int = 4096):
        """
        Initialize audio capture.
        
        Args:
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels (1 for mono)
            chunk_size: Number of frames per chunk
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.stream = None
        self.is_recording = False
        self.audio_buffer = deque(maxlen=sample_rate * 10)  # 10 second buffer
        self.recording_data = np.array([])
        self.frame_count = 0
        
    def start_recording(self):
        """Start capturing audio from microphone."""
        try:
            def audio_callback(indata, frames, time_info, status):
                if status:
                    print(f"Audio capture status: {status}")
                
                audio_chunk = indata[:, 0].copy()
                self.audio_buffer.extend(audio_chunk)
                self.recording_data = np.append(self.recording_data, audio_chunk)
                self.frame_count += 1
            
            self.stream = sd.InputStream(
                channels=self.channels,
                samplerate=self.sample_rate,
                blocksize=self.chunk_size,
                callback=audio_callback
            )
            self.stream.start()
            self.is_recording = True
            return True
        except Exception as e:
            print(f"Error starting audio recording: {e}")
            return False
    
    def stop_recording(self):
        """Stop capturing audio."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
        self.is_recording = False
    
    def get_audio_data(self) -> np.ndarray:
        """Get recorded audio data."""
        return self.recording_data
    
    def save_audio(self, filepath: str):
        """Save recorded audio to file."""
        if len(self.recording_data) > 0:
            sf.write(filepath, self.recording_data, self.sample_rate)
            return True
        return False
    
    def get_current_buffer(self) -> np.ndarray:
        """Get current audio buffer for processing."""
        return np.array(list(self.audio_buffer))


class SpeechMetricsCalculator:
    """Calculates speech metrics like speaking rate, pitch, energy, etc."""
    
    def __init__(self, sample_rate: int = 16000):
        """Initialize speech metrics calculator."""
        self.sample_rate = sample_rate
        
    def calculate_speaking_rate(self, audio: np.ndarray) -> Dict:
        """
        Estimate speaking rate from audio.
        
        Args:
            audio: Audio data
            
        Returns:
            Speaking rate metrics
        """
        try:
            # Detect speech onset/offset
            S = librosa.feature.melspectrogram(y=audio, sr=self.sample_rate)
            S_db = librosa.power_to_db(S, ref=np.max)
            
            # Simple energy-based voice activity detection
            energy = np.mean(S_db, axis=0)
            threshold = np.mean(energy) + np.std(energy)
            
            # Estimate speech segments
            speech_frames = np.sum(energy > threshold)
            total_frames = len(energy)
            
            # Convert to time
            frame_length = 512
            hop_length = 512
            total_time = librosa.frames_to_time(total_frames, sr=self.sample_rate, hop_length=hop_length)
            speech_time = librosa.frames_to_time(speech_frames, sr=self.sample_rate, hop_length=hop_length)
            
            # Estimate words per minute (typical word = 0.5 sec)
            estimated_words = speech_time / 0.5
            words_per_minute = (estimated_words / total_time * 60) if total_time > 0 else 0
            
            return {
                'words_per_minute': max(0, min(300, words_per_minute)),  # 60-180 WPM typical
                'speech_proportion': speech_time / total_time if total_time > 0 else 0,
                'total_speech_seconds': speech_time,
                'total_duration_seconds': total_time
            }
        except Exception as e:
            print(f"Error calculating speaking rate: {e}")
            return {'words_per_minute': 0, 'speech_proportion': 0, 'total_speech_seconds': 0}
    
    def calculate_pitch_statistics(self, audio: np.ndarray) -> Dict:
        """
        Calculate pitch-based metrics for voice quality.
        
        Args:
            audio: Audio data
            
        Returns:
            Pitch statistics
        """
        try:
            # Estimate pitch using autocorrelation
            D = librosa.stft(audio)
            magnitude = np.abs(D)
            
            # Extract some pitch features
            onset_env = librosa.onset.onset_strength(y=audio, sr=self.sample_rate)
            
            # Calculate spectral properties
            spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=self.sample_rate)[0]
            
            return {
                'avg_spectral_centroid': float(np.mean(spectral_centroids)),
                'std_spectral_centroid': float(np.std(spectral_centroids)),
                'avg_spectral_rolloff': float(np.mean(spectral_rolloff)),
                'pitch_variance': float(np.std(spectral_centroids))  # High variance = variety in pitch
            }
        except Exception as e:
            print(f"Error calculating pitch: {e}")
            return {
                'avg_spectral_centroid': 0,
                'avg_spectral_rolloff': 0,
                'pitch_variance': 0
            }
    
    def calculate_energy(self, audio: np.ndarray) -> Dict:
        """
        Calculate energy-based metrics (loudness, consistency).
        
        Args:
            audio: Audio data
            
        Returns:
            Energy metrics
        """
        try:
            # RMS Energy
            rms_energy = np.sqrt(np.mean(audio ** 2))
            
            # MFCC (Mel-frequency cepstral coefficients)
            mfcc = librosa.feature.mfcc(y=audio, sr=self.sample_rate, n_mfcc=13)
            
            return {
                'rms_energy': float(rms_energy),
                'avg_mfcc_energy': float(np.mean(mfcc[0])),  # First MFCC coefficient
                'energy_consistency': float(1.0 - (np.std(mfcc[0]) / (np.mean(np.abs(mfcc[0])) + 0.001)))
            }
        except Exception as e:
            print(f"Error calculating energy: {e}")
            return {'rms_energy': 0, 'avg_mfcc_energy': 0, 'energy_consistency': 0}
    
    def detect_filler_words(self, text: str) -> Dict:
        """
        Detect filler words and speech patterns in transcribed text.
        
        Args:
            text: Transcribed speech text
            
        Returns:
            Filler word statistics
        """
        filler_words = {
            'um': 0, 'uh': 0, 'like': 0, 'you know': 0,
            'sort of': 0, 'kind of': 0, 'basically': 0,
            'literally': 0, 'actually': 0
        }
        
        text_lower = text.lower()
        
        for filler in filler_words:
            filler_words[filler] = text_lower.count(filler)
        
        total_fillers = sum(filler_words.values())
        words = len(text.split())
        
        return {
            'filler_words': filler_words,
            'total_fillers': total_fillers,
            'filler_word_density': total_fillers / words if words > 0 else 0,
            'speech_clarity_score': 1.0 - min(1.0, total_fillers / max(1, words))
        }


class SentimentAnalyzer:
    """Analyzes sentiment and tone from text transcriptions."""
    
    def __init__(self):
        """Initialize sentiment analyzer."""
        try:
            from transformers import pipeline
            self.sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased")
            self.use_transformers = True
        except Exception as e:
            print(f"Transformers not available, using fallback: {e}")
            self.use_transformers = False
            self._init_textblob()
    
    def _init_textblob(self):
        """Initialize TextBlob as fallback."""
        try:
            from textblob import TextBlob
            self.textblob = TextBlob
        except ImportError:
            self.textblob = None
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text.
        
        Returns:
            Sentiment analysis with scores
        """
        if not text.strip():
            return {
                'sentiment': 'neutral',
                'positive_score': 0.33,
                'negative_score': 0.33,
                'neutral_score': 0.34,
                'confidence': 0.0
            }
        
        if self.use_transformers:
            try:
                result = self.sentiment_pipeline(text[:512])[0]  # Limit to 512 chars
                label = result['label'].lower()
                score = result['score']
                
                return {
                    'sentiment': label,
                    'positive_score': score if label == 'positive' else 1 - score,
                    'negative_score': score if label == 'negative' else 1 - score,
                    'neutral_score': 1 - max(score, 1 - score),
                    'confidence': score
                }
            except Exception as e:
                print(f"Error in transformer sentiment: {e}")
                return self._fallback_sentiment(text)
        else:
            return self._fallback_sentiment(text)
    
    def _fallback_sentiment(self, text: str) -> Dict:
        """Fallback sentiment analysis using keywords."""
        positive_words = {'good', 'great', 'excellent', 'happy', 'love', 'best', 'amazing', 'wonderful'}
        negative_words = {'bad', 'terrible', 'hate', 'awful', 'horrible', 'worst', 'disappointed'}
        
        text_lower = set(text.lower().split())
        
        positive_count = len(text_lower & positive_words)
        negative_count = len(text_lower & negative_words)
        total = positive_count + negative_count
        
        if total == 0:
            return {
                'sentiment': 'neutral',
                'positive_score': 0.33,
                'negative_score': 0.33,
                'neutral_score': 0.34,
                'confidence': 0.0
            }
        
        pos_score = positive_count / total
        neg_score = negative_count / total
        
        sentiment = 'positive' if pos_score > neg_score else 'negative' if neg_score > pos_score else 'neutral'
        
        return {
            'sentiment': sentiment,
            'positive_score': pos_score,
            'negative_score': neg_score,
            'neutral_score': 1 - pos_score - neg_score,
            'confidence': max(pos_score, neg_score)
        }
    
    def extract_key_phrases(self, text: str, num_phrases: int = 5) -> List[str]:
        """Extract key phrases from text (simple version)."""
        words = text.split()
        # Simple approach: use longer sequences
        phrases = []
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            if len(phrase) > 10:  # Reasonable length
                phrases.append(phrase)
        
        # Return most common phrases
        from collections import Counter
        return [phrase for phrase, count in Counter(phrases).most_common(num_phrases)]


class AudioTranscriptionEngine:
    """Handles audio transcription."""
    
    def __init__(self):
        """Initialize transcription engine."""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.use_speech_recognition = True
        except ImportError:
            print("speech_recognition not available")
            self.use_speech_recognition = False
    
    def transcribe_audio(self, audio_data: np.ndarray, sample_rate: int = 16000) -> Dict:
        """
        Transcribe audio to text.
        
        Args:
            audio_data: Audio waveform
            sample_rate: Sample rate in Hz
            
        Returns:
            Transcription results
        """
        if not self.use_speech_recognition:
            return {
                'text': '[Transcription unavailable - speech_recognition not installed]',
                'confidence': 0.0,
                'segments': []
            }
        
        try:
            import speech_recognition as sr
            from io import BytesIO
            
            # Convert audio to WAV format in memory
            wav_buffer = BytesIO()
            sf.write(wav_buffer, audio_data, sample_rate, format='WAV')
            wav_buffer.seek(0)
            
            # Transcribe
            with sr.AudioFile(wav_buffer) as source:
                audio = self.recognizer.record(source)
            
            try:
                text = self.recognizer.recognize_google(audio)
                return {
                    'text': text,
                    'confidence': 0.9,
                    'segments': []
                }
            except sr.UnknownValueError:
                return {
                    'text': '[Speech not understood]',
                    'confidence': 0.0,
                    'segments': []
                }
            except sr.RequestError as e:
                return {
                    'text': f'[Transcription error: {str(e)}]',
                    'confidence': 0.0,
                    'segments': []
                }
        except Exception as e:
            print(f"Transcription error: {e}")
            return {
                'text': '[Transcription failed]',
                'confidence': 0.0,
                'segments': []
            }


class InterviewAudioAnalyzer:
    """Combined audio analysis for interviews."""
    
    def __init__(self, sample_rate: int = 16000):
        """Initialize audio analyzer."""
        self.audio_capture = RealTimeAudioCapture(sample_rate=sample_rate)
        self.speech_metrics = SpeechMetricsCalculator(sample_rate=sample_rate)
        self.sentiment_analyzer = SentimentAnalyzer()
        self.transcription_engine = AudioTranscriptionEngine()
        self.sample_rate = sample_rate
        self.analysis_history = deque(maxlen=100)
    
    def analyze_audio_chunk(self, audio_data: np.ndarray) -> Dict:
        """
        Analyze a chunk of audio.
        
        Args:
            audio_data: Audio waveform
            
        Returns:
            Complete audio analysis
        """
        if len(audio_data) == 0:
            return {}
        
        # Get base metrics
        speech_rate = self.speech_metrics.calculate_speaking_rate(audio_data)
        pitch_stats = self.speech_metrics.calculate_pitch_statistics(audio_data)
        energy_stats = self.speech_metrics.calculate_energy(audio_data)
        
        analysis = {
            'timestamp': datetime.now(),
            'speech_metrics': {
                **speech_rate,
                **pitch_stats,
                **energy_stats
            }
        }
        
        # Transcribe and analyze sentiment (if text available)
        transcription = self.transcription_engine.transcribe_audio(audio_data, self.sample_rate)
        analysis['transcription'] = transcription['text']
        
        if transcription['text'] and not transcription['text'].startswith('['):
            filler_analysis = self.speech_metrics.detect_filler_words(transcription['text'])
            sentiment_analysis = self.sentiment_analyzer.analyze_sentiment(transcription['text'])
            
            analysis['filler_words'] = filler_analysis
            analysis['sentiment'] = sentiment_analysis
            analysis['key_phrases'] = self.sentiment_analyzer.extract_key_phrases(
                transcription['text']
            )
        
        self.analysis_history.append(analysis)
        return analysis
    
    def get_session_summary(self) -> Dict:
        """Get summary of audio analysis for entire session."""
        if not self.analysis_history:
            return {}
        
        analyses = list(self.analysis_history)
        
        # Aggregate speech metrics
        speech_rates = [a['speech_metrics'].get('words_per_minute', 0) for a in analyses]
        pitch_variances = [a['speech_metrics'].get('pitch_variance', 0) for a in analyses]
        energy_levels = [a['speech_metrics'].get('rms_energy', 0) for a in analyses]
        
        return {
            'total_analysis_chunks': len(analyses),
            'avg_speaking_rate': float(np.mean(speech_rates)) if speech_rates else 0,
            'avg_pitch_variance': float(np.mean(pitch_variances)) if pitch_variances else 0,
            'avg_energy': float(np.mean(energy_levels)) if energy_levels else 0,
            'speech_clarity_score': np.mean([
                a.get('filler_words', {}).get('speech_clarity_score', 1.0) 
                for a in analyses
            ]),
            'sentiment_distribution': self._get_sentiment_distribution(analyses)
        }
    
    def _get_sentiment_distribution(self, analyses: List[Dict]) -> Dict:
        """Calculate sentiment distribution across session."""
        sentiments = defaultdict(int)
        total = 0
        
        for a in analyses:
            if 'sentiment' in a:
                sentiment = a['sentiment'].get('sentiment', 'neutral')
                sentiments[sentiment] += 1
                total += 1
        
        if total == 0:
            return {'positive': 0, 'negative': 0, 'neutral': 100}
        
        return {
            sent: (count / total * 100) for sent, count in sentiments.items()
        }
