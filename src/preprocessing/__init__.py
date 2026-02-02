"""
Preprocessing package for medical transcripts.

This package provides utilities for cleaning and structuring
medical transcription text before NLP processing.

Components:
    - TextCleaner: Clean and normalize text
    - SpeakerDiarizer: Separate doctor/patient dialogue
    - TemporalExtractor: Extract dates, times, durations
"""

from .text_cleaner import TextCleaner
from .speaker_diarization import SpeakerDiarizer
from .temporal_extractor import TemporalExtractor

__all__ = [
    'TextCleaner',
    'SpeakerDiarizer',
    'TemporalExtractor',
]