"""Unit tests for NER module."""
import pytest
from src.models.ner import ScispaCyNER

def test_ner_initialization():
    """Test NER initializes successfully."""
    ner = ScispaCyNER()
    assert ner.nlp is not None

def test_extract_entities():
    """Test entity extraction."""
    ner = ScispaCyNER()
    text = "Patient has neck pain and received physiotherapy"
    entities = ner.extract_entities(text)
    
    assert 'symptoms' in entities
    assert 'treatments' in entities
    assert len(entities['symptoms']) > 0

def test_extract_diagnosis():
    """Test diagnosis extraction."""
    ner = ScispaCyNER()
    text = "Patient was diagnosed with whiplash injury"
    diagnosis = ner.extract_diagnosis(text)
    
    assert diagnosis is not None
    assert 'whiplash' in diagnosis.lower()

if __name__ == "__main__":
    pytest.main([__file__, '-v'])