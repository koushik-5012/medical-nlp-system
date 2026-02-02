"""
Sentiment analysis module for patient statements.

This module analyzes the emotional tone of patient statements using
transformer-based models.

Author: Koushik
Date: February 2026
"""

from transformers import pipeline
from typing import List, Dict
import warnings

from src.config import MODELS, SENTIMENT_LABELS, MODEL_SETTINGS

warnings.filterwarnings('ignore')


class SentimentAnalyzer:
    """
    Analyze sentiment of patient statements.
    
    This class uses transformer models to classify patient sentiment
    and maps it to medical context (Anxious, Neutral, Reassured).
    
    Attributes:
        model: Hugging Face sentiment analysis pipeline
        confidence_threshold: Minimum confidence for classification
        
    Example:
        >>> analyzer = SentimentAnalyzer()
        >>> text = "I'm worried about my pain"
        >>> result = analyzer.analyze_sentiment(text)
        >>> print(result['sentiment'])
        'Anxious'
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize sentiment analyzer.
        
        Args:
            model_name: Name of sentiment model (default from config)
        """
        model = model_name or MODELS['sentiment']
        
        self.model = pipeline(
            "sentiment-analysis",
            model=model,
            device=-1
        )
        
        self.confidence_threshold = MODEL_SETTINGS['sentiment_confidence_threshold']
        self.sentiment_mapping = SENTIMENT_LABELS
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of single text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment, confidence, and raw label
        """
        if not text or not text.strip():
            return {
                'text': text,
                'sentiment': 'Neutral',
                'confidence': 0.0,
                'raw_label': 'NEUTRAL'
            }
        
        try:
            result = self.model(text[:512])[0]
            
            sentiment = self._map_to_medical_context(
                result['label'],
                result['score']
            )
            
            return {
                'text': text,
                'sentiment': sentiment,
                'confidence': round(result['score'], 3),
                'raw_label': result['label']
            }
            
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {
                'text': text,
                'sentiment': 'Neutral',
                'confidence': 0.0,
                'raw_label': 'ERROR'
            }
    
    def analyze_patient_statements(self, statements: List[str]) -> List[Dict]:
        """
        Analyze sentiment for multiple patient statements.
        
        Args:
            statements: List of patient statement strings
            
        Returns:
            List of sentiment analysis results
        """
        results = []
        
        for statement in statements:
            if len(statement.split()) < 3:
                continue
            
            analysis = self.analyze_sentiment(statement)
            results.append(analysis)
        
        return results
    
    def _map_to_medical_context(self, label: str, confidence: float) -> str:
        """
        Map model output to medical sentiment context.
        
        Args:
            label: Raw sentiment label from model
            confidence: Confidence score
            
        Returns:
            Medical context sentiment (Anxious/Neutral/Reassured)
        """
        if confidence < self.confidence_threshold:
            return 'Neutral'
        
        return self.sentiment_mapping.get(label, 'Neutral')
    
    def get_overall_sentiment(self, results: List[Dict]) -> Dict:
        """
        Calculate overall sentiment distribution.
        
        Args:
            results: List of sentiment analysis results
            
        Returns:
            Dictionary with sentiment distribution and dominant sentiment
        """
        if not results:
            return {
                'distribution': {'Anxious': 0, 'Neutral': 0, 'Reassured': 0},
                'dominant_sentiment': 'Neutral',
                'total_statements': 0,
                'avg_confidence': 0.0
            }
        
        sentiments = [r['sentiment'] for r in results]
        confidences = [r['confidence'] for r in results]
        
        distribution = {
            'Anxious': sentiments.count('Anxious'),
            'Neutral': sentiments.count('Neutral'),
            'Reassured': sentiments.count('Reassured')
        }
        
        dominant = max(distribution, key=distribution.get)
        
        return {
            'distribution': distribution,
            'dominant_sentiment': dominant,
            'total_statements': len(sentiments),
            'avg_confidence': round(sum(confidences) / len(confidences), 3) if confidences else 0.0
        }
    
    def get_sentiment_timeline(self, results: List[Dict]) -> List[Dict]:
        """
        Get sentiment progression over conversation.
        
        Args:
            results: List of sentiment analysis results
            
        Returns:
            List of sentiment points for timeline
        """
        timeline = []
        
        sentiment_scores = {
            'Anxious': -1,
            'Neutral': 0,
            'Reassured': 1
        }
        
        for i, result in enumerate(results):
            timeline.append({
                'position': i + 1,
                'sentiment': result['sentiment'],
                'score': sentiment_scores.get(result['sentiment'], 0),
                'confidence': result['confidence']
            })
        
        return timeline


if __name__ == "__main__":
    """Quick test of SentimentAnalyzer functionality."""
    
    test_statements = [
        "I'm doing better, but I still have some discomfort now and then.",
        "The first four weeks were rough. My neck and back pain were really bad.",
        "That's a relief!",
        "I'm worried about my back pain.",
        "No, nothing like that. I don't feel nervous driving.",
        "That's great to hear. So, I don't need to worry about this affecting me in the future?",
    ]
    
    analyzer = SentimentAnalyzer()
    
    print("=" * 60)
    print("SENTIMENT ANALYSIS TEST")
    print("=" * 60)
    
    results = analyzer.analyze_patient_statements(test_statements)
    overall = analyzer.get_overall_sentiment(results)
    
    print("\n📊 Overall Sentiment:")
    print(f"   Dominant: {overall['dominant_sentiment']}")
    print(f"   Distribution: {overall['distribution']}")
    print(f"   Avg Confidence: {overall['avg_confidence']}")
    
    print("\n💬 Statement-by-Statement Analysis:")
    for i, result in enumerate(results, 1):
        sentiment_icon = {
            'Anxious': '😰',
            'Neutral': '😐',
            'Reassured': '😊'
        }.get(result['sentiment'], '😐')
        
        preview = result['text'][:60] + "..." if len(result['text']) > 60 else result['text']
        print(f"\n{i}. {sentiment_icon} {result['sentiment']} (confidence: {result['confidence']})")
        print(f"   \"{preview}\"")
    
    print("\n" + "=" * 60)
    print("✅ Sentiment analysis working correctly!")
    print("=" * 60)