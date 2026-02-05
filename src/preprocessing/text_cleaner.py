"""
Text cleaning module for medical transcripts.

This module provides utilities to clean and normalize raw medical
transcription text before NLP processing.

Author: Koushik
Date: February 2026
"""

import re
from typing import Dict, Optional

from src.config import MEDICAL_ABBREVIATIONS


# ============================================================================
# TEXT CLEANER CLASS
# ============================================================================
class TextCleaner:
    """
    Clean and normalize medical transcription text.
    
    This class handles various text cleaning operations including:
    - Whitespace normalization
    - Punctuation cleaning
    - Markdown artifact removal
    - Medical abbreviation expansion
    
    Example:
        >>> cleaner = TextCleaner()
        >>> text = "**Patient:**  Extra   spaces here..."
        >>> clean_text = cleaner.clean(text)
    """
    
    def __init__(self):
        """Initialize the text cleaner with regex patterns."""
        # Compile regex patterns for efficiency
        self.patterns = {
            'extra_spaces': re.compile(r'\s+'),
            'markdown': re.compile(r'\*+'),
            'speaker_tags': re.compile(r'\*\*(.*?)\*\*:'),
        }
        
        # Medical abbreviations from config
        self.abbreviations = MEDICAL_ABBREVIATIONS
    def clean(self, text: str) -> str:
        """
        Apply all cleaning operations to text.
        
        Args:
            text: Raw transcription text
            
        Returns:
            Cleaned and normalized text
            
        Example:
            >>> cleaner = TextCleaner()
            >>> cleaner.clean("**Patient:**  I have  pain")
            'Patient: I have pain'
        """
        if not text or not text.strip():
            return ""
        
        # Apply cleaning steps in order
        text = self._remove_markdown(text)
        text = self._normalize_whitespace(text)
        text = self._normalize_punctuation(text)
        text = self._expand_abbreviations(text)
        
        return text.strip()
    def _remove_markdown(self, text: str) -> str:
        """
        Remove markdown formatting artifacts.
        
        Args:
            text: Text with potential markdown
            
        Returns:
            Text without markdown symbols
        """
        # Remove ** around speaker names and emphasis
        text = self.patterns['markdown'].sub('', text)
        return text
    
    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize all whitespace to single spaces.
        
        Args:
            text: Text with irregular whitespace
            
        Returns:
            Text with normalized spacing
        """
        # Replace multiple spaces/tabs/newlines with single space
        text = self.patterns['extra_spaces'].sub(' ', text)
        return text
    def _normalize_punctuation(self, text: str) -> str:
        """
        Normalize punctuation marks.
        
        Args:
            text: Text with various punctuation
            
        Returns:
            Text with normalized punctuation
        """
        # Normalize different dash types
        text = text.replace('—', '-').replace('–', '-')
        
        # Normalize ellipsis
        text = text.replace('…', '...')
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        return text
    
    def _expand_abbreviations(self, text: str) -> str:
        """
        Expand common medical abbreviations.
        
        Args:
            text: Text containing abbreviations
            
        Returns:
            Text with expanded abbreviations
        """
        for abbr, expansion in self.abbreviations.items():
            # Use word boundaries to avoid partial matches
            pattern = rf'\b{re.escape(abbr)}\b'
            text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)
        
        return text
    def clean_for_display(self, text: str, max_length: int = 100) -> str:
        """
        Clean text and truncate for display purposes.
        
        Args:
            text: Text to clean
            max_length: Maximum length for display
            
        Returns:
            Cleaned and truncated text
        """
        cleaned = self.clean(text)
        
        if len(cleaned) > max_length:
            return cleaned[:max_length] + "..."
        
        return cleaned
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    """Quick test of TextCleaner functionality."""
    
    # Sample messy text
    test_text = """
    **Physician:** Good  morning,   Ms. Jones.
    **Patient:**  I went to  A&E  yesterday...
    """
    
    # Initialize cleaner
    cleaner = TextCleaner()
    
    # Clean text
    cleaned = cleaner.clean(test_text)
    
    # Display results
    print("=" * 60)
    print("TEXT CLEANER TEST")
    print("=" * 60)
    print("\nOriginal:")
    print(repr(test_text))
    print("\nCleaned:")
    print(cleaned)
    print("\n" + "=" * 60)