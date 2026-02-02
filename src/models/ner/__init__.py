"""
Named Entity Recognition package for medical text.

This package provides NER capabilities for extracting medical entities
from transcripts.

Components:
    - BaseNER: Abstract base class for NER implementations
    - ScispaCyNER: Medical NER using scispaCy
    - EntityValidator: Validation and cleaning utilities
"""

from .base_ner import BaseNER
from .scispacy_ner import ScispaCyNER
from .entity_validator import EntityValidator

__all__ = [
    'BaseNER',
    'ScispaCyNER',
    'EntityValidator',
]
