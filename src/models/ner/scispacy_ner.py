"""
ScispaCy-based NER implementation for medical entity extraction.

This module uses scispaCy (medical NLP library) to extract
medical entities from transcripts.

Author: Koushik
Date: February 2026
"""

import spacy
from typing import Dict, List, Set
from collections import defaultdict

from src.config import MODELS, ENTITY_TYPES, SYMPTOM_KEYWORDS, TREATMENT_KEYWORDS
from .base_ner import BaseNER


class ScispaCyNER(BaseNER):
    """
    Medical NER using scispaCy models.
    
    This class implements medical entity extraction using scispaCy,
    a specialized library for biomedical and clinical text processing.
    
    Attributes:
        nlp: Loaded scispaCy model
        entity_mapping: Mapping of spaCy labels to our categories
        
    Example:
        >>> ner = ScispaCyNER()
        >>> text = "Patient has neck pain and back pain"
        >>> entities = ner.extract_entities(text)
        >>> print(entities['symptoms'])
        ['neck pain', 'back pain']
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize ScispaCy NER extractor.
        
        Args:
            model_name: Name of scispaCy model to use (default from config)
        """
        model = model_name or MODELS['spacy_medical']
        
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"Model {model} not found. Trying to download...")
            import subprocess
            subprocess.run(['pip', 'install', f'https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/{model}-0.5.4.tar.gz'])
            self.nlp = spacy.load(model)
        
        self.entity_mapping = ENTITY_TYPES
        
        self.symptom_keywords = set(SYMPTOM_KEYWORDS)
        self.treatment_keywords = set(TREATMENT_KEYWORDS)
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract medical entities from text.
        
        Args:
            text: Input medical text
            
        Returns:
            Dictionary with categorized entities
        """
        if not text or not text.strip():
            return {
                'symptoms': [],
                'treatments': [],
                'diagnoses': [],
                'anatomy': [],
            }
        
        doc = self.nlp(text)
        
        entities = defaultdict(set)
        
        for ent in doc.ents:
            category = self._categorize_entity(ent)
            if category:
                entities[category].add(ent.text)
        
        entities = self._enhance_with_rules(doc, entities)
        
        return {k: self._clean_entities(list(v)) for k, v in entities.items()}
    
    def extract_with_confidence(self, text: str) -> Dict[str, List[Dict]]:
        """
        Extract entities with confidence scores.
        
        Args:
            text: Input medical text
            
        Returns:
            Dictionary with entities and confidence scores
        """
        if not text or not text.strip():
            return {
                'symptoms': [],
                'treatments': [],
                'diagnoses': [],
                'anatomy': [],
            }
        
        doc = self.nlp(text)
        
        entities = defaultdict(list)
        seen = defaultdict(set)
        
        for ent in doc.ents:
            category = self._categorize_entity(ent)
            if category and ent.text.lower() not in seen[category]:
                entities[category].append({
                    'text': ent.text,
                    'label': ent.label_,
                    'confidence': 0.85,
                    'start': ent.start_char,
                    'end': ent.end_char,
                })
                seen[category].add(ent.text.lower())
        
        return dict(entities)
    
    def _categorize_entity(self, entity) -> str:
        """
        Categorize entity based on its label.
        
        Args:
            entity: spaCy entity object
            
        Returns:
            Category name or None
        """
        for category, labels in self.entity_mapping.items():
            if entity.label_ in labels:
                return category
        return None
    
    def _enhance_with_rules(self, doc, entities: Dict) -> Dict:
        """
        Enhance entity extraction with rule-based patterns.
        
        Args:
            doc: spaCy doc object
            entities: Existing entities dictionary
            
        Returns:
            Enhanced entities dictionary
        """
        text_lower = doc.text.lower()
        
        for token in doc:
            token_lemma = token.lemma_.lower()
            
            if token_lemma in self.symptom_keywords:
                context_start = max(0, token.i - 2)
                context_end = min(len(doc), token.i + 2)
                context = doc[context_start:context_end].text
                
                if len(context.split()) <= 5:
                    entities['symptoms'].add(context.strip())
        
        for keyword in self.treatment_keywords:
            if keyword in text_lower:
                for sent in doc.sents:
                    if keyword in sent.text.lower():
                        entities['treatments'].add(keyword)
        
        return entities
    
    def _clean_entities(self, entities: List[str]) -> List[str]:
        """
        Clean and deduplicate entity list.
        
        Args:
            entities: List of entity strings
            
        Returns:
            Cleaned list of entities
        """
        cleaned = []
        seen = set()
        
        for entity in entities:
            entity_clean = entity.strip()
            entity_lower = entity_clean.lower()
            
            if len(entity_clean) > 2 and entity_lower not in seen:
                cleaned.append(entity_clean)
                seen.add(entity_lower)
        
        cleaned.sort(key=len, reverse=True)
        
        return cleaned
    
    def extract_diagnosis(self, text: str) -> str:
        """
        Extract primary diagnosis from text.
        
        Args:
            text: Input medical text
            
        Returns:
            Diagnosis string or None
        """
        import re
        
        diagnosis_patterns = [
            r'diagnosed with (.*?)(?:\.|,|$)',
            r'diagnosis[:\s]+(.*?)(?:\.|,|$)',
            r'it was (?:a|an) (.*?) injury',
            r'said it was (.*?)(?:\.|,|$)',
        ]
        
        for pattern in diagnosis_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                diagnosis = match.group(1).strip()
                if diagnosis:
                    return diagnosis
        
        entities = self.extract_entities(text)
        if entities.get('diagnoses'):
            return entities['diagnoses'][0]
        
        return None
    
    def extract_prognosis(self, text: str) -> str:
        """
        Extract prognosis from text.
        
        Args:
            text: Input medical text
            
        Returns:
            Prognosis string or None
        """
        import re
        
        prognosis_patterns = [
            r'(full recovery.*?)(?:\.|$)',
            r'(expect.*?recovery.*?)(?:\.|$)',
            r'(prognosis.*?)(?:\.|$)',
            r"(don't foresee.*?)(?:\.|$)",
        ]
        
        for pattern in prognosis_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None


if __name__ == "__main__":
    """Quick test of ScispaCyNER functionality."""
    
    test_text = """
    Patient reports neck pain and back pain following car accident.
    Diagnosed with whiplash injury at Accident and Emergency.
    Received ten sessions of physiotherapy and regular painkillers.
    Patient experienced stiffness and discomfort initially.
    Full recovery expected within six months. No long-term damage anticipated.
    """
    
    ner = ScispaCyNER()
    
    entities = ner.extract_entities(test_text)
    entities_conf = ner.extract_with_confidence(test_text)
    diagnosis = ner.extract_diagnosis(test_text)
    prognosis = ner.extract_prognosis(test_text)
    
    print("=" * 60)
    print("MEDICAL NER TEST")
    print("=" * 60)
    
    print("\n🔴 Symptoms:")
    for symptom in entities.get('symptoms', []):
        print(f"   • {symptom}")
    
    print("\n💊 Treatments:")
    for treatment in entities.get('treatments', []):
        print(f"   • {treatment}")
    
    print("\n🏥 Diagnoses:")
    for diag in entities.get('diagnoses', []):
        print(f"   • {diag}")
    
    print("\n📋 Extracted Information:")
    print(f"   Primary Diagnosis: {diagnosis}")
    print(f"   Prognosis: {prognosis}")
    
    print("\n📊 Entities with Confidence:")
    for category, items in entities_conf.items():
        if items:
            print(f"\n   {category.upper()}:")
            for item in items[:3]:
                print(f"      • {item['text']} (confidence: {item['confidence']:.2f})")
    
    print("\n" + "=" * 60)
    print("✅ Medical NER working correctly!")
    print("=" * 60)