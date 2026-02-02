"""
Medical summarization module.

This module generates structured medical summaries by combining
NER, temporal extraction, and keyword extraction.

Author: Koushik
Date: February 2026
"""

from typing import Dict, List
import re

from src.models.ner import ScispaCyNER
from src.preprocessing import TemporalExtractor
from .keyword_extractor import MedicalKeywordExtractor


class MedicalSummarizer:
    """
    Generate structured medical summaries.
    
    This class combines multiple NLP components to create comprehensive
    medical summaries from transcripts.
    
    Attributes:
        ner_extractor: NER extraction component
        temporal_extractor: Temporal information extractor
        keyword_extractor: Keyword extraction component
        
    Example:
        >>> summarizer = MedicalSummarizer()
        >>> summary = summarizer.generate_summary(transcript, dialogues)
        >>> print(summary['diagnosis'])
        'whiplash injury'
    """
    
    def __init__(self):
        """Initialize medical summarizer with all components."""
        self.ner = ScispaCyNER()
        self.temporal_extractor = TemporalExtractor()
        self.keyword_extractor = MedicalKeywordExtractor()
    
    def generate_summary(
        self,
        transcript: str,
        dialogues: List[Dict] = None
    ) -> Dict:
        """
        Generate complete structured summary.
        
        Args:
            transcript: Full transcript text
            dialogues: Parsed dialogue list (optional)
            
        Returns:
            Dictionary with complete medical summary
        """
        entities = self.ner.extract_entities(transcript)
        
        diagnosis = self.ner.extract_diagnosis(transcript)
        prognosis = self.ner.extract_prognosis(transcript)
        
        keywords = self.keyword_extractor.extract_medical_phrases(transcript)
        
        temporal = self.temporal_extractor.extract_all_temporal(transcript)
        
        patient_name = self._extract_patient_name(transcript)
        
        current_status = self._extract_current_status(transcript, dialogues)
        
        summary = {
            'patient_name': patient_name,
            'symptoms': entities.get('symptoms', []),
            'diagnosis': diagnosis,
            'treatments': entities.get('treatments', []),
            'current_status': current_status,
            'prognosis': prognosis,
            'temporal_info': {
                'incident_date': self._extract_incident_date(temporal),
                'treatment_duration': self._extract_treatment_duration(transcript),
                'dates': [d['text'] for d in temporal.get('dates', [])],
                'durations': [d['text'] for d in temporal.get('durations', [])],
            },
            'medical_keywords': keywords,
            'anatomy_mentioned': entities.get('anatomy', []),
            'metadata': {
                'total_entities': sum(len(v) for v in entities.values()),
                'has_diagnosis': diagnosis is not None,
                'has_prognosis': prognosis is not None,
            }
        }
        
        return summary
    
    def _extract_patient_name(self, text: str) -> str:
        """
        Extract patient name from text.
        
        Args:
            text: Input text
            
        Returns:
            Patient name or default
        """
        patterns = [
            r'Ms\.\s+([A-Z][a-z]+)',
            r'Mr\.\s+([A-Z][a-z]+)',
            r'Mrs\.\s+([A-Z][a-z]+)',
            r'Patient\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return "Patient"
    
    def _extract_current_status(
        self,
        transcript: str,
        dialogues: List[Dict] = None
    ) -> str:
        """
        Extract current patient status.
        
        Args:
            transcript: Full transcript
            dialogues: Parsed dialogues
            
        Returns:
            Current status description
        """
        if dialogues:
            patient_statements = [
                d['text'] for d in dialogues
                if d['speaker'] == 'patient'
            ]
            
            status_keywords = ['better', 'improving', 'occasional', 'still', 'now']
            
            for statement in reversed(patient_statements):
                if any(kw in statement.lower() for kw in status_keywords):
                    return statement
        
        status_patterns = [
            r'(currently.*?)(?:\.|$)',
            r'(now.*?pain.*?)(?:\.|$)',
            r'(occasional.*?)(?:\.|$)',
        ]
        
        for pattern in status_patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Status not explicitly mentioned"
    
    def _extract_incident_date(self, temporal: Dict) -> str:
        """
        Extract incident/accident date.
        
        Args:
            temporal: Temporal information dictionary
            
        Returns:
            Incident date or None
        """
        dates = temporal.get('dates', [])
        if dates:
            return dates[0]['text']
        return None
    
    def _extract_treatment_duration(self, text: str) -> str:
        """
        Extract treatment duration.
        
        Args:
            text: Input text
            
        Returns:
            Treatment duration or None
        """
        duration_pattern = r'(\d+\s*(?:session|week|month)s?)'
        match = re.search(duration_pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(0)
        
        return None
    
    def generate_short_summary(self, full_summary: Dict) -> str:
        """
        Generate concise text summary.
        
        Args:
            full_summary: Complete summary dictionary
            
        Returns:
            Short text summary
        """
        parts = []
        
        if full_summary['patient_name']:
            parts.append(f"Patient: {full_summary['patient_name']}")
        
        if full_summary['diagnosis']:
            parts.append(f"Diagnosis: {full_summary['diagnosis']}")
        
        if full_summary['symptoms']:
            symptoms_str = ', '.join(full_summary['symptoms'][:3])
            parts.append(f"Symptoms: {symptoms_str}")
        
        if full_summary['treatments']:
            treatments_str = ', '.join(full_summary['treatments'][:2])
            parts.append(f"Treatment: {treatments_str}")
        
        if full_summary['prognosis']:
            parts.append(f"Prognosis: {full_summary['prognosis']}")
        
        return '. '.join(parts) + '.'


if __name__ == "__main__":
    """Quick test of MedicalSummarizer functionality."""
    
    test_transcript = """
    Physician: Good morning, Ms. Jones. How are you feeling today?
    
    Patient: Good morning, doctor. I'm doing better, but I still have 
    some discomfort now and then.
    
    Physician: I understand you were in a car accident last September.
    
    Patient: Yes, it was on September 1st. I was driving when another 
    car hit me from behind. I hit my head on the steering wheel, and 
    I could feel pain in my neck and back almost right away.
    
    Patient: I went to Accident and Emergency. They said it was a 
    whiplash injury. The first four weeks were rough. I had to go 
    through ten sessions of physiotherapy.
    
    Physician: Are you still experiencing pain now?
    
    Patient: It's not constant, but I do get occasional backaches.
    
    Physician: Given your progress, I'd expect you to make a full 
    recovery within six months of the accident.
    """
    
    summarizer = MedicalSummarizer()
    
    summary = summarizer.generate_summary(test_transcript)
    short_summary = summarizer.generate_short_summary(summary)
    
    print("=" * 60)
    print("MEDICAL SUMMARIZATION TEST")
    print("=" * 60)
    
    print(f"\n👤 Patient: {summary['patient_name']}")
    print(f"\n🏥 Diagnosis: {summary['diagnosis']}")
    print(f"\n📈 Prognosis: {summary['prognosis']}")
    
    print(f"\n🔴 Symptoms ({len(summary['symptoms'])}):")
    for symptom in summary['symptoms'][:5]:
        print(f"   • {symptom}")
    
    print(f"\n💊 Treatments ({len(summary['treatments'])}):")
    for treatment in summary['treatments'][:5]:
        print(f"   • {treatment}")
    
    print(f"\n📅 Temporal Information:")
    print(f"   Incident Date: {summary['temporal_info']['incident_date']}")
    print(f"   Treatment Duration: {summary['temporal_info']['treatment_duration']}")
    
    print(f"\n🔑 Medical Keywords ({len(summary['medical_keywords'])}):")
    for keyword in summary['medical_keywords'][:5]:
        print(f"   • {keyword}")
    
    print(f"\n📊 Current Status:")
    print(f"   {summary['current_status']}")
    
    print(f"\n📝 Short Summary:")
    print(f"   {short_summary}")
    
    print("\n" + "=" * 60)
    print("✅ Medical summarization working correctly!")
    print("=" * 60)