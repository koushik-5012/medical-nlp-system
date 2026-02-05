"""
Medical NER using scispaCy models.

Author: Koushik
Date: February 2026
"""

import spacy
from typing import Dict, List
import re
import warnings

from src.config import MODELS, ENTITY_TYPES, SYMPTOM_KEYWORDS, TREATMENT_KEYWORDS

warnings.filterwarnings('ignore')


class ScispaCyNER:
    """Medical NER using scispaCy models."""
    
    def __init__(self):
        """Initialize with fallback to en_core_web_sm if scispacy unavailable."""
        model = MODELS.get('spacy_medical', 'en_core_sci_md')
        
        try:
            self.nlp = spacy.load(model)
            print(f"✅ Loaded medical model: {model}")
        except OSError:
            print(f"⚠️ Medical model not found, using general model as fallback")
            try:
                self.nlp = spacy.load('en_core_web_sm')
                print("✅ Loaded en_core_web_sm")
            except OSError:
                print("Downloading en_core_web_sm...")
                import subprocess
                subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
                self.nlp = spacy.load('en_core_web_sm')
        
        self.entity_mapping = ENTITY_TYPES
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract medical entities from text."""
        if not text or not text.strip():
            return {'symptoms': [], 'treatments': [], 'diagnoses': [], 'anatomy': []}
        
        doc = self.nlp(text)
        
        entities = {
            'symptoms': [],
            'treatments': [],
            'diagnoses': [],
            'anatomy': []
        }
        
        for ent in doc.ents:
            category = self._categorize_entity(ent.label_)
            if category and ent.text.strip():
                entities[category].append(ent.text.strip())
        
        entities = self._enhance_with_rules(text, entities)
        entities = self._clean_entities(entities)
        
        return entities
    
    def extract_with_confidence(self, text: str) -> Dict[str, List[Dict]]:
        """Extract entities with confidence scores."""
        if not text or not text.strip():
            return {'symptoms': [], 'treatments': [], 'diagnoses': [], 'anatomy': []}
        
        doc = self.nlp(text)
        
        entities = {
            'symptoms': [],
            'treatments': [],
            'diagnoses': [],
            'anatomy': []
        }
        
        for ent in doc.ents:
            category = self._categorize_entity(ent.label_)
            if category:
                entities[category].append({
                    'text': ent.text.strip(),
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'confidence': 0.85
                })
        
        return entities
    
    def _categorize_entity(self, label: str) -> str:
        """Map spaCy entity labels to categories."""
        for category, labels in self.entity_mapping.items():
            if label in labels:
                return category
        return None
    
    def _enhance_with_rules(self, text: str, entities: Dict) -> Dict:
        """Add rule-based entity extraction."""
        text_lower = text.lower()
        
        for symptom in SYMPTOM_KEYWORDS:
            pattern = rf'\b{symptom}\b'
            if re.search(pattern, text_lower):
                entities['symptoms'].append(symptom)
        
        for treatment in TREATMENT_KEYWORDS:
            pattern = rf'\b{treatment}\b'
            if re.search(pattern, text_lower):
                entities['treatments'].append(treatment)
        
        return entities
    
    def _clean_entities(self, entities: Dict) -> Dict:
        """Clean and deduplicate entities."""
        cleaned = {}
        
        for category, entity_list in entities.items():
            seen = set()
            unique = []
            
            for entity in entity_list:
                entity_clean = entity.lower().strip()
                if entity_clean and len(entity_clean) > 2 and entity_clean not in seen:
                    unique.append(entity)
                    seen.add(entity_clean)
            
            unique.sort(key=len, reverse=True)
            cleaned[category] = unique[:20]
        
        return cleaned
    
    def extract_diagnosis(self, text: str) -> str:
        """Extract diagnosis from text."""
        patterns = [
            r'diagnosed with\s+([^,.]+)',
            r'diagnosis[:\s]+([^,.]+)',
            r'it was (?:a|an)\s+([^,.]+?)\s+injury',
            r'consistent with\s+([^,.]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def extract_prognosis(self, text: str) -> str:
        """Extract prognosis information."""
        patterns = [
            r'(full recovery.*?)(?:\.|$)',
            r'(expect.*?recovery.*?)(?:\.|$)',
            r"(don't foresee.*?)(?:\.|$)",
            r'(prognosis.*?)(?:\.|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None


if __name__ == "__main__":
    """Test NER extraction."""
    test_text = """
    Patient reports neck pain and back pain following car accident.
    Diagnosed with whiplash injury. Received physiotherapy and painkillers.
    Full recovery expected within six months.
    """
    
    ner = ScispaCyNER()
    
    entities = ner.extract_entities(test_text)
    diagnosis = ner.extract_diagnosis(test_text)
    prognosis = ner.extract_prognosis(test_text)
    
    print("=" * 60)
    print("NER TEST")
    print("=" * 60)
    
    for category, items in entities.items():
        if items:
            print(f"\n{category.upper()}:")
            for item in items:
                print(f"   • {item}")
    
    print(f"\nDiagnosis: {diagnosis}")
    print(f"Prognosis: {prognosis}")
    
    print("\n✅ NER working!")
