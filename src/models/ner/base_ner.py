"""
Base NER module defining interface for entity extraction.

This module provides an abstract base class that defines the
interface for all NER implementations.

Author: Koushik
Date: February 2026
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class BaseNER(ABC):
    """
    Abstract base class for Named Entity Recognition.
    
    This class defines the interface that all NER implementations
    must follow. It ensures consistency across different NER approaches.
    
    Example:
        >>> class MyNER(BaseNER):
        ...     def extract_entities(self, text):
        ...         return {'symptoms': ['pain']}
    """
    
    @abstractmethod
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract medical entities from text.
        
        Args:
            text: Input medical text
            
        Returns:
            Dictionary with entity categories as keys and lists of entities as values
            
        Example:
            {
                'symptoms': ['neck pain', 'back pain'],
                'treatments': ['physiotherapy'],
                'diagnoses': ['whiplash injury']
            }
        """
        pass
    
    @abstractmethod
    def extract_with_confidence(self, text: str) -> Dict[str, List[Dict]]:
        """
        Extract entities with confidence scores.
        
        Args:
            text: Input medical text
            
        Returns:
            Dictionary with entities and their confidence scores
            
        Example:
            {
                'symptoms': [
                    {'text': 'neck pain', 'confidence': 0.95},
                    {'text': 'back pain', 'confidence': 0.92}
                ]
            }
        """
        pass