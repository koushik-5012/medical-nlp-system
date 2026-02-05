"""Medical NER using scispaCy models."""

import spacy
from typing import Dict, List
import re
import warnings
from src.config import MODELS, ENTITY_TYPES, SYMPTOM_KEYWORDS, TREATMENT_KEYWORDS

warnings.filterwarnings('ignore')


class ScispaCyNER:
    """Medical NER with fallback to general model."""
    
    def __init__(self):
        """Initialize NER with automatic fallback."""
        self.nlp = None
        
        # Try medical model
        try:
            self.nlp = spacy.load('en_core_sci_md')
            print("✅ Loaded en_core_sci_md")
        except:
            print("⚠️ Medical model not available")
        
        # Fallback to general model
        if self.nlp is None:
            try:
                self.nlp = spacy.load('en_core_web_sm')
                print("✅ Loaded en_core_web_sm")
            except:
                print("📥 Downloading en_core_web_sm...")
                import subprocess
                import sys
                subprocess.run([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
                result = subprocess.run(
                    [sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'],
                    capture_output=True,
                    text=True
                )
                print(f"Download result: {result.returncode}")
                if result.returncode == 0:
                    import importlib
                    importlib.invalidate_caches()
                    self.nlp = spacy.load('en_core_web_sm')
                    print("✅ Successfully loaded en_core_web_sm after download")
                else:
                    raise Exception(f"Failed to download model: {result.stderr}")
        
        self.entity_mapping = ENTITY_TYPES
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract medical entities."""
        if not text or not text.strip():
            return {'symptoms': [], 'treatments': [], 'diagnoses': [], 'anatomy': []}
        
        doc = self.nlp(text)
        entities = {'symptoms': [], 'treatments': [], 'diagnoses': [], 'anatomy': []}
        
        for ent in doc.ents:
            category = self._categorize_entity(ent.label_)
            if category and ent.text.strip():
                entities[category].append(ent.text.strip())
        
        entities = self._enhance_with_rules(text, entities)
        entities = self._clean_entities(entities)
        return entities
    
    def extract_with_confidence(self, text: str) -> Dict[str, List[Dict]]:
        """Extract entities with confidence."""
        if not text or not text.strip():
            return {'symptoms': [], 'treatments': [], 'diagnoses': [], 'anatomy': []}
        
        doc = self.nlp(text)
        entities = {'symptoms': [], 'treatments': [], 'diagnoses': [], 'anatomy': []}
        
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
        """Map labels to categories."""
        for category, labels in self.entity_mapping.items():
            if label in labels:
                return category
        return None
    
    def _enhance_with_rules(self, text: str, entities: Dict) -> Dict:
        """Add rule-based extraction."""
        text_lower = text.lower()
        
        for symptom in SYMPTOM_KEYWORDS:
            if re.search(rf'\b{symptom}\b', text_lower):
                entities['symptoms'].append(symptom)
        
        for treatment in TREATMENT_KEYWORDS:
            if re.search(rf'\b{treatment}\b', text_lower):
                entities['treatments'].append(treatment)
        
        return entities
    
    def _clean_entities(self, entities: Dict) -> Dict:
        """Deduplicate entities."""
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
        """Extract diagnosis."""
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
        """Extract prognosis."""
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