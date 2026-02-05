"""Unit tests for pipeline."""
import pytest
from src.pipeline.medical_nlp_pipeline import MedicalNLPPipeline

def test_pipeline_initialization():
    """Test pipeline initializes."""
    pipeline = MedicalNLPPipeline()
    assert pipeline.ner is not None
    assert pipeline.sentiment_analyzer is not None

def test_pipeline_process():
    """Test pipeline processes text."""
    pipeline = MedicalNLPPipeline()
    text = "Patient: I have neck pain. Doctor: I see."
    result = pipeline.process(text)
    
    assert 'entities' in result
    assert 'sentiment_analysis' in result
    assert 'summary' in result

if __name__ == "__main__":
    pytest.main([__file__, '-v'])