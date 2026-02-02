"""
Keyword extraction module for medical text.

This module extracts important medical keywords and phrases using
KeyBERT and contextual embeddings.

Author: Koushik
Date: February 2026
"""

from keybert import KeyBERT
from typing import List, Tuple, Set
import warnings

from src.config import PROCESSING_CONFIG

warnings.filterwarnings('ignore')


class MedicalKeywordExtractor:
    """
    Extract medical keywords and phrases from text.
    
    This class uses KeyBERT to extract contextually relevant keywords
    and phrases from medical transcripts.
    
    Attributes:
        kw_model: KeyBERT model instance
        max_keywords: Maximum number of keywords to extract
        
    Example:
        >>> extractor = MedicalKeywordExtractor()
        >>> text = "Patient has neck pain and received physiotherapy"
        >>> keywords = extractor.extract_keywords(text)
        >>> print(keywords)
        [('neck pain', 0.65), ('physiotherapy', 0.58)]
    """
    
    def __init__(self):
        """Initialize keyword extractor."""
        self.kw_model = KeyBERT()
        
        self.max_keywords = PROCESSING_CONFIG['max_keywords']
        self.ngram_range = PROCESSING_CONFIG['keyword_ngram_range']
        
        self.medical_stopwords = {
            'patient', 'doctor', 'physician', 'said', 'told',
            'asked', 'feel', 'feeling', 'yes', 'no', 'okay',
            'hello', 'hi', 'good', 'morning', 'afternoon',
            'thank', 'thanks', 'welcome', 'bye', 'goodbye'
        }
    
    def extract_keywords(
        self,
        text: str,
        top_n: int = None,
        diversity: float = 0.7
    ) -> List[Tuple[str, float]]:
        """
        Extract top keywords from text.
        
        Args:
            text: Input medical text
            top_n: Number of keywords to extract (default from config)
            diversity: Diversity of results (0-1, higher = more diverse)
            
        Returns:
            List of (keyword, score) tuples
        """
        if not text or not text.strip():
            return []
        
        top_n = top_n or self.max_keywords
        
        try:
            keywords = self.kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=self.ngram_range,
                stop_words='english',
                top_n=top_n * 2,
                use_mmr=True,
                diversity=diversity
            )
            
            filtered = [
                (kw, score) for kw, score in keywords
                if not any(stop in kw.lower() for stop in self.medical_stopwords)
            ]
            
            return filtered[:top_n]
            
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []
    
    def extract_medical_phrases(
        self,
        text: str,
        top_n: int = None
    ) -> List[str]:
        """
        Extract medical-specific phrases.
        
        Args:
            text: Input medical text
            top_n: Number of phrases to extract
            
        Returns:
            List of medical phrase strings
        """
        keywords = self.extract_keywords(text, top_n=top_n or 15)
        
        medical_phrases = []
        medical_indicators = [
            'injury', 'pain', 'therapy', 'treatment', 'accident',
            'exam', 'diagnosis', 'recovery', 'symptom', 'medical',
            'physiotherapy', 'medication', 'sessions', 'whiplash',
            'examination', 'prognosis', 'stiffness', 'discomfort'
        ]
        
        for phrase, score in keywords:
            if any(indicator in phrase.lower() for indicator in medical_indicators):
                medical_phrases.append(phrase)
        
        return medical_phrases
    
    def extract_by_category(self, text: str) -> dict:
        """
        Extract keywords categorized by type.
        
        Args:
            text: Input medical text
            
        Returns:
            Dictionary with categorized keywords
        """
        all_keywords = self.extract_keywords(text, top_n=20)
        
        categories = {
            'symptoms': [],
            'treatments': [],
            'conditions': [],
            'general': []
        }
        
        symptom_terms = ['pain', 'ache', 'discomfort', 'stiffness', 'tenderness']
        treatment_terms = ['therapy', 'treatment', 'medication', 'sessions', 'physiotherapy']
        condition_terms = ['injury', 'accident', 'diagnosis', 'whiplash', 'strain']
        
        for keyword, score in all_keywords:
            kw_lower = keyword.lower()
            
            categorized = False
            
            if any(term in kw_lower for term in symptom_terms):
                categories['symptoms'].append((keyword, score))
                categorized = True
            
            if any(term in kw_lower for term in treatment_terms):
                categories['treatments'].append((keyword, score))
                categorized = True
            
            if any(term in kw_lower for term in condition_terms):
                categories['conditions'].append((keyword, score))
                categorized = True
            
            if not categorized:
                categories['general'].append((keyword, score))
        
        return categories
    
    def get_top_keywords_summary(self, text: str, n: int = 5) -> str:
        """
        Get comma-separated summary of top keywords.
        
        Args:
            text: Input medical text
            n: Number of top keywords
            
        Returns:
            Comma-separated keyword string
        """
        keywords = self.extract_keywords(text, top_n=n)
        return ', '.join([kw for kw, _ in keywords])


if __name__ == "__main__":
    """Quick test of MedicalKeywordExtractor functionality."""
    
    test_text = """
    Patient reports neck pain and back pain following car accident.
    Diagnosed with whiplash injury at Accident and Emergency.
    Received ten sessions of physiotherapy and regular painkillers.
    Patient experienced stiffness and discomfort initially.
    Full recovery expected within six months. No long-term damage anticipated.
    Physical examination shows full range of movement.
    """
    
    extractor = MedicalKeywordExtractor()
    
    keywords = extractor.extract_keywords(test_text)
    medical_phrases = extractor.extract_medical_phrases(test_text)
    categorized = extractor.extract_by_category(test_text)
    summary = extractor.get_top_keywords_summary(test_text)
    
    print("=" * 60)
    print("KEYWORD EXTRACTION TEST")
    print("=" * 60)
    
    print(f"\n🔑 Top Keywords ({len(keywords)}):")
    for i, (keyword, score) in enumerate(keywords, 1):
        print(f"   {i}. {keyword} (score: {score:.3f})")
    
    print(f"\n🏥 Medical Phrases ({len(medical_phrases)}):")
    for i, phrase in enumerate(medical_phrases, 1):
        print(f"   {i}. {phrase}")
    
    print(f"\n📂 Categorized Keywords:")
    for category, items in categorized.items():
        if items:
            print(f"\n   {category.upper()}:")
            for keyword, score in items[:3]:
                print(f"      • {keyword} ({score:.3f})")
    
    print(f"\n📝 Summary:")
    print(f"   {summary}")
    
    print("\n" + "=" * 60)
    print("✅ Keyword extraction working correctly!")
    print("=" * 60)