"""
Constants and terminology for Medical NLP System.

This module contains medical-specific constants including:
- Entity type definitions
- Medical term mappings
- SOAP section keywords

Author: Koushik
Date: February 2026
"""

# ============================================================================
# MEDICAL ENTITY TYPES
# ============================================================================

# Entity categories for NER
ENTITY_TYPES = {
    'symptoms': ['SIGN_SYMPTOM', 'DISEASE_DISORDER'],
    'treatments': ['THERAPEUTIC_PROCEDURE', 'MEDICATION'],
    'anatomy': ['BODY_PART_ORGAN', 'TISSUE'],
    'tests': ['DIAGNOSTIC_PROCEDURE', 'LAB_VALUE'],
}

# Common symptom keywords
SYMPTOM_KEYWORDS = [
    'pain', 'ache', 'discomfort', 'stiffness', 'tenderness',
    'soreness', 'hurt', 'burning', 'throbbing', 'sharp',
    'dull', 'chronic', 'acute', 'severe', 'mild',
]

# Common treatment keywords
TREATMENT_KEYWORDS = [
    'physiotherapy', 'therapy', 'treatment', 'medication',
    'painkillers', 'analgesics', 'sessions', 'procedure',
    'surgery', 'prescription', 'dose', 'regimen',
]


# ============================================================================
# SOAP NOTE KEYWORDS
# ============================================================================

# Keywords for SOAP section classification
SOAP_KEYWORDS = {
    'subjective': [
        'feel', 'felt', 'feeling', 'pain', 'discomfort', 'worried',
        'concerned', 'started', 'happened', 'noticed', 'experiencing',
        'suffering', 'complaining', 'reports', 'states', 'describes',
    ],
    'objective': [
        'examination', 'exam', 'observed', 'noted', 'range of motion',
        'tenderness', 'normal', 'abnormal', 'vital signs', 'appears',
        'inspection', 'palpation', 'auscultation', 'findings',
    ],
    'assessment': [
        'diagnosis', 'diagnosed', 'condition', 'prognosis', 'recovery',
        'improvement', 'severity', 'acute', 'chronic', 'mild', 'moderate',
        'severe', 'stable', 'unstable', 'likely', 'probable',
    ],
    'plan': [
        'treatment', 'recommend', 'prescribe', 'follow-up', 'continue',
        'return', 'if', 'monitor', 'schedule', 'refer', 'therapy',
        'medication', 'instructions', 'advised', 'counseled',
    ],
}


# ============================================================================
# MEDICAL ABBREVIATIONS
# ============================================================================

# Common medical abbreviations and their expansions
MEDICAL_ABBREVIATIONS = {
    'A&E': 'Accident and Emergency',
    'pt': 'patient',
    'pts': 'patients',
    'dr': 'doctor',
    'hx': 'history',
    'tx': 'treatment',
    'rx': 'prescription',
    'sx': 'symptoms',
    'dx': 'diagnosis',
    'ROM': 'range of motion',
    'BP': 'blood pressure',
    'HR': 'heart rate',
    'resp': 'respiration',
}


# ============================================================================
# TEMPORAL PATTERNS
# ============================================================================

# Regex patterns for temporal information
TEMPORAL_PATTERNS = {
    'duration': r'(\d+)\s*(week|month|day|year)s?',
    'date': r'(\w+\s+\d{1,2}(?:st|nd|rd|th)?)',
    'time': r'(\d{1,2}):(\d{2})\s*(am|pm|AM|PM)?',
}