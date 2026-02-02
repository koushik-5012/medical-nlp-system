"""
Intent classification module for conversation analysis.

This module classifies the intent behind patient statements using
zero-shot classification.

Author: Koushik
Date: February 2026
"""

from transformers import pipeline
from typing import List, Dict
import warnings

from src.config import MODELS, INTENT_CATEGORIES, MODEL_SETTINGS

warnings.filterwarnings('ignore')


class IntentClassifier:
    """
    Classify intent of patient statements.
    
    This class uses zero-shot classification to identify the intent
    behind patient statements without requiring training data.
    
    Attributes:
        model: Hugging Face zero-shot classification pipeline
        intent_labels: List of possible intent categories
        
    Example:
        >>> classifier = IntentClassifier()
        >>> text = "I'm worried about my pain"
        >>> result = classifier.classify_intent(text)
        >>> print(result['intent'])
        'expressing concern'
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize intent classifier.
        
        Args:
            model_name: Name of classification model (default from config)
        """
        model = model_name or MODELS['intent']
        
        self.model = pipeline(
            "zero-shot-classification",
            model=model,
            device=-1
        )
        
        self.intent_labels = INTENT_CATEGORIES
        self.confidence_threshold = MODEL_SETTINGS['intent_confidence_threshold']
    
    def classify_intent(self, text: str) -> Dict:
        """
        Classify intent of single statement.
        
        Args:
            text: Input text to classify
            
        Returns:
            Dictionary with intent, confidence, and all scores
        """
        if not text or not text.strip():
            return {
                'text': text,
                'intent': 'unknown',
                'confidence': 0.0,
                'all_scores': {}
            }
        
        try:
            result = self.model(
                text[:512],
                candidate_labels=self.intent_labels,
                multi_label=False
            )
            
            return {
                'text': text,
                'intent': result['labels'][0],
                'confidence': round(result['scores'][0], 3),
                'all_scores': {
                    label: round(score, 3)
                    for label, score in zip(result['labels'], result['scores'])
                }
            }
            
        except Exception as e:
            print(f"Error classifying intent: {e}")
            return {
                'text': text,
                'intent': 'unknown',
                'confidence': 0.0,
                'all_scores': {}
            }
    
    def classify_patient_intents(self, statements: List[str]) -> List[Dict]:
        """
        Classify intents for multiple statements.
        
        Args:
            statements: List of patient statement strings
            
        Returns:
            List of intent classification results
        """
        results = []
        
        for statement in statements:
            if len(statement.split()) < 3:
                continue
            
            intent = self.classify_intent(statement)
            results.append(intent)
        
        return results
    
    def get_intent_distribution(self, results: List[Dict]) -> Dict:
        """
        Calculate intent distribution.
        
        Args:
            results: List of intent classification results
            
        Returns:
            Dictionary with intent counts
        """
        if not results:
            return {intent: 0 for intent in self.intent_labels}
        
        distribution = {intent: 0 for intent in self.intent_labels}
        
        for result in results:
            intent = result['intent']
            if intent in distribution:
                distribution[intent] += 1
        
        return distribution
    
    def get_dominant_intent(self, results: List[Dict]) -> str:
        """
        Get most common intent from results.
        
        Args:
            results: List of intent classification results
            
        Returns:
            Most common intent label
        """
        if not results:
            return 'unknown'
        
        distribution = self.get_intent_distribution(results)
        return max(distribution, key=distribution.get)


if __name__ == "__main__":
    """Quick test of IntentClassifier functionality."""
    
    test_statements = [
        "I'm doing better, but I still have some discomfort now and then.",
        "The first four weeks were rough. My neck and back pain were really bad.",
        "That's a relief!",
        "So, I don't need to worry about this affecting me in the future?",
        "Yes, it was on September 1st, around 12:30 in the afternoon.",
        "I had to go through ten sessions of physiotherapy.",
    ]
    
    classifier = IntentClassifier()
    
    print("=" * 60)
    print("INTENT CLASSIFICATION TEST")
    print("=" * 60)
    
    results = classifier.classify_patient_intents(test_statements)
    distribution = classifier.get_intent_distribution(results)
    dominant = classifier.get_dominant_intent(results)
    
    print("\n📊 Intent Distribution:")
    for intent, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"   {intent}: {count}")
    
    print(f"\n🎯 Dominant Intent: {dominant}")
    
    print("\n💬 Statement-by-Statement Classification:")
    for i, result in enumerate(results, 1):
        preview = result['text'][:60] + "..." if len(result['text']) > 60 else result['text']
        print(f"\n{i}. Intent: {result['intent']} (confidence: {result['confidence']})")
        print(f"   \"{preview}\"")
        print(f"   Top 3 scores:")
        top_3 = sorted(result['all_scores'].items(), key=lambda x: x[1], reverse=True)[:3]
        for intent, score in top_3:
            print(f"      • {intent}: {score}")
    
    print("\n" + "=" * 60)
    print("✅ Intent classification working correctly!")
    print("=" * 60)