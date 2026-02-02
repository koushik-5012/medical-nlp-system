"""
Configuration module for Medical NLP System.

This module contains all project-wide settings including:
- File paths and directories
- Model configurations
- Processing parameters

Author: Koushik
Date: February 2026
"""

import os
from pathlib import Path

# ============================================================================
# PROJECT PATHS
# ============================================================================
# Get the project root directory (medical-nlp-system/)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / 'data'
DATA_RAW = DATA_DIR / 'raw'
DATA_PROCESSED = DATA_DIR / 'processed'
DATA_OUTPUT = DATA_DIR / 'output'
DATA_EXAMPLES = DATA_DIR / 'examples'

# Model directories
MODELS_DIR = PROJECT_ROOT / 'models'

# Logs directory
LOGS_DIR = PROJECT_ROOT / 'logs'

# Ensure directories exist
DATA_OUTPUT.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# MODEL CONFIGURATIONS
# ===========================================================================
# NLP Models
MODELS = {
    'spacy_general': 'en_core_web_sm',
    'spacy_medical': 'en_core_sci_md',
    'sentiment': 'distilbert-base-uncased-finetuned-sst-2-english',
    'intent': 'facebook/bart-large-mnli',
}

# Model-specific settings
MODEL_SETTINGS = {
    'sentiment_confidence_threshold': 0.7,
    'intent_confidence_threshold': 0.6,
    'ner_confidence_threshold': 0.5,
}


# ============================================================================
# PROCESSING CONFIGURATIONS
# ============================================================================
# Text processing parameters
PROCESSING_CONFIG = {
    'min_statement_length': 3,           # Minimum words in a statement
    'max_text_length': 50000,            # Maximum characters to process
    'max_keywords': 15,                  # Maximum keywords to extract
    'keyword_ngram_range': (1, 3),       # Keyword phrase length (1-3 words)
    'similarity_threshold': 0.7,         # For entity deduplication
}

# Sentiment labels mapping
SENTIMENT_LABELS = {
    'POSITIVE': 'Reassured',
    'NEGATIVE': 'Anxious',
    'NEUTRAL': 'Neutral',
}

# Intent categories
INTENT_CATEGORIES = [
    "seeking reassurance",
    "reporting symptoms",
    "expressing concern",
    "asking questions",
    "describing history",
    "confirming understanding",
    "expressing relief",
]


# ============================================================================
# OUTPUT CONFIGURATIONS
# ============================================================================
#output formats
OUTPUT_CONFIG = {
    'include_confidence_scores': True,
    'include_metadata': True,
    'pretty_print_json': True,
    'json_indent': 2,
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',                     # DEBUG, INFO, WARNING, ERROR
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': LOGS_DIR / 'pipeline.log',
}