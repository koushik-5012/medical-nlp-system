# Technical Documentation

## 📚 Module Reference

### Configuration Module

#### `src/config/config.py`

**Purpose:** Centralized project configuration

**Exports:**
```python
PROJECT_ROOT: Path          # Auto-detected project root
DATA_DIR: Path              # Data directory path
MODELS_DIR: Path            # Models directory path
LOGS_DIR: Path              # Logs directory path
DATA_RAW: Path              # Raw data path
DATA_PROCESSED: Path        # Processed data path
DATA_OUTPUT: Path           # Output data path

MODELS: Dict[str, str]      # Model name mappings
MODEL_SETTINGS: Dict        # Model thresholds and params
SENTIMENT_LABELS: Dict      # Sentiment label mappings
INTENT_CATEGORIES: List     # Intent classification labels
PROCESSING_CONFIG: Dict     # Processing parameters
OUTPUT_CONFIG: Dict         # Output formatting settings
LOGGING_CONFIG: Dict        # Logging configuration
```

#### `src/config/constants.py`

**Purpose:** Medical domain constants

**Exports:**
```python
ENTITY_TYPES: Dict[str, List[str]]       # spaCy → category mapping
SYMPTOM_KEYWORDS: List[str]              # Symptom detection keywords
TREATMENT_KEYWORDS: List[str]            # Treatment detection keywords
SOAP_KEYWORDS: Dict[str, List[str]]      # SOAP section keywords
MEDICAL_ABBREVIATIONS: Dict[str, str]    # Medical abbreviation expansions
TEMPORAL_PATTERNS: Dict[str, str]        # Regex patterns for temporal extraction
```

---

### Preprocessing Module

#### `TextCleaner`

**Import:**
```python
from src.preprocessing import TextCleaner
```

**Usage:**
```python
cleaner = TextCleaner()
cleaned_text = cleaner.clean(raw_text)
preview = cleaner.clean_for_display(text, max_length=500)
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `clean(text)` | `text: str` | `str` | Full text cleaning |
| `clean_for_display(text, max_length)` | `text: str, max_length: int` | `str` | Truncated preview |

---

#### `SpeakerDiarizer`

**Import:**
```python
from src.preprocessing import SpeakerDiarizer
```

**Usage:**
```python
diarizer = SpeakerDiarizer()
dialogues = diarizer.parse_transcript(text)
patient_statements = diarizer.get_patient_statements(dialogues)
stats = diarizer.get_dialogue_stats(dialogues)
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `parse_transcript(text)` | `text: str` | `List[Dict]` | Parse speaker turns |
| `get_patient_statements(dialogues)` | `dialogues: List[Dict]` | `List[str]` | Extract patient text |
| `get_doctor_statements(dialogues)` | `dialogues: List[Dict]` | `List[str]` | Extract doctor text |
| `get_dialogue_stats(dialogues)` | `dialogues: List[Dict]` | `Dict` | Get statistics |

**Output Format:**
```python
[
  {'speaker': 'doctor', 'text': '...'},
  {'speaker': 'patient', 'text': '...'}
]
```

---

#### `TemporalExtractor`

**Import:**
```python
from src.preprocessing import TemporalExtractor
```

**Usage:**
```python
extractor = TemporalExtractor()
temporal = extractor.extract_all_temporal(text)
incident_date = extractor.extract_incident_date(text)
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `extract_all_temporal(text)` | `text: str` | `Dict` | Extract all temporal info |
| `extract_incident_date(text)` | `text: str` | `Optional[str]` | Get incident date |
| `extract_treatment_duration(text)` | `text: str` | `Optional[str]` | Get treatment duration |

**Output Format:**
```python
{
  'dates': [{'text': 'September 1st', 'position': (10, 23), 'type': 'date'}],
  'times': [{'text': '12:30 PM', 'position': (45, 53), 'type': 'time'}],
  'durations': [{'text': '4 weeks', 'position': (100, 107), 'type': 'duration'}]
}
```

---

### NER Module

#### `ScispaCyNER`

**Import:**
```python
from src.models.ner import ScispaCyNER
```

**Usage:**
```python
ner = ScispaCyNER()
entities = ner.extract_entities(text)
entities_conf = ner.extract_with_confidence(text)
diagnosis = ner.extract_diagnosis(text)
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `extract_entities(text)` | `text: str` | `Dict[str, List[str]]` | Extract entities |
| `extract_with_confidence(text)` | `text: str` | `Dict[str, List[Dict]]` | With confidence scores |
| `extract_diagnosis(text)` | `text: str` | `Optional[str]` | Extract diagnosis |
| `extract_prognosis(text)` | `text: str` | `Optional[str]` | Extract prognosis |

**Output Format:**
```python
{
  'symptoms': ['neck pain', 'back pain'],
  'treatments': ['physiotherapy', 'painkillers'],
  'diagnoses': ['whiplash injury'],
  'anatomy': ['neck', 'back']
}
```

---

### Sentiment & Intent Modules

#### `SentimentAnalyzer`

**Import:**
```python
from src.models.sentiment import SentimentAnalyzer
```

**Usage:**
```python
analyzer = SentimentAnalyzer()
results = analyzer.analyze_patient_statements(statements)
overall = analyzer.get_overall_sentiment(results)
```

**Output:**
```python
{
  'text': '...',
  'sentiment': 'Anxious' | 'Neutral' | 'Reassured',
  'confidence': 0.85,
  'raw_label': 'NEGATIVE'
}
```

---

#### `IntentClassifier`

**Import:**
```python
from src.models.intent import IntentClassifier
```

**Usage:**
```python
classifier = IntentClassifier()
intent = classifier.classify_intent(statement)
distribution = classifier.get_intent_distribution(results)
```

**Output:**
```python
{
  'text': '...',
  'intent': 'seeking reassurance',
  'confidence': 0.75,
  'all_scores': {...}
}
```

---

### Pipeline Module

#### `MedicalNLPPipeline`

**Import:**
```python
from src.pipeline import MedicalNLPPipeline
```

**Usage:**
```python
pipeline = MedicalNLPPipeline()
result = pipeline.process(transcript_text)
pipeline.save_output(result, 'output.json')
```

**Complete Output Structure:**
```python
{
  "metadata": {
    "processed_at": "2026-02-05T12:00:00",
    "pipeline_version": "1.0.0",
    "total_dialogues": 12
  },
  "summary": {
    "patient_name": "Ms. Jones",
    "symptoms": [...],
    "diagnosis": "...",
    "treatments": [...],
    "current_status": "...",
    "prognosis": "..."
  },
  "entities": {...},
  "temporal_info": {...},
  "sentiment_analysis": {...},
  "intent_analysis": {...},
  "keywords": {...},
  "dialogues": [...]
}
```

---

## 📊 Performance Metrics

### Processing Benchmarks

**Test Environment:**
- MacBook Air M1, 8GB RAM
- Python 3.10
- All models loaded in memory

**Results:**

| Transcript Size | Processing Time | Memory Usage |
|----------------|-----------------|--------------|
| 500 words | 3.2s | 1.8GB |
| 1000 words | 4.5s | 1.9GB |
| 2000 words | 6.8s | 2.1GB |

### Accuracy Metrics

| Component | Metric | Value |
|-----------|--------|-------|
| NER | Precision | ~85% |
| NER | Recall | ~80% |
| Sentiment | Accuracy | ~82% |
| Intent | Accuracy | ~78% |

---

## 💡 Usage Examples

### Example 1: Basic Pipeline Usage
```python
from src.pipeline import MedicalNLPPipeline

# Initialize
pipeline = MedicalNLPPipeline()

# Load transcript
with open('transcript.txt', 'r') as f:
    text = f.read()

# Process
result = pipeline.process(text)

# Access results
print(f"Diagnosis: {result['summary']['diagnosis']}")
print(f"Symptoms: {result['entities']['symptoms']}")
print(f"Overall Sentiment: {result['sentiment_analysis']['overall']['dominant_sentiment']}")
```

### Example 2: Custom NER Extraction
```python
from src.models.ner import ScispaCyNER, EntityValidator

# Initialize
ner = ScispaCyNER()
validator = EntityValidator()

# Extract
entities = ner.extract_entities(text)

# Validate
validated = validator.validate_entities_dict(entities)

print(validated)
```

### Example 3: SOAP Note Generation
```python
from src.generators import SOAPGenerator
from src.preprocessing import SpeakerDiarizer

# Initialize
generator = SOAPGenerator()
diarizer = SpeakerDiarizer()

# Parse
dialogues = diarizer.parse_transcript(text)

# Generate
soap = generator.generate(text, dialogues)

# Format
formatted = generator.to_formatted_text(soap)
print(formatted)
```

---

## 🔧 Configuration Guide

### Adjusting Thresholds

Edit `src/config/config.py`:
```python
MODEL_SETTINGS = {
    'sentiment_confidence_threshold': 0.7,  # Lower = more classifications
    'intent_confidence_threshold': 0.6,
    'ner_confidence_threshold': 0.5,
}
```

### Adding New Intent Categories

Edit `src/config/config.py`:
```python
INTENT_CATEGORIES = [
    'seeking reassurance',
    'reporting symptoms',
    # Add your new intent here
    'requesting prescription',
]
```

### Adding New Medical Keywords

Edit `src/config/constants.py`:
```python
SYMPTOM_KEYWORDS = [
    'pain', 'ache', 'discomfort',
    # Add your symptom keywords
    'fatigue', 'nausea',
]
```

---

## 🐛 Troubleshooting

### Issue: Model Not Found

**Error:** `OSError: [E050] Can't find model 'en_core_web_sm'`

**Solution:**
```bash
python -m spacy download en_core_web_sm
```

### Issue: Memory Error

**Error:** `MemoryError: Unable to allocate array`

**Solution:**
- Reduce `max_keywords` in config
- Process shorter transcripts
- Increase system RAM

### Issue: Slow Processing

**Solution:**
- Enable GPU support for transformers
- Reduce model batch sizes
- Cache loaded models

---

## 📦 Dependencies

### Core Dependencies
```
streamlit>=1.28.0          # Web framework
spacy>=3.7.0              # NLP core
scispacy>=0.5.4           # Medical NLP
transformers>=4.36.0      # Deep learning models
torch>=2.1.0              # PyTorch backend
keybert>=0.7.0            # Keyword extraction
plotly>=5.18.0            # Visualizations
Pillow>=10.0.0            # Image processing
```

### Development Dependencies
```
pytest>=7.4.0             # Testing framework
black>=23.0.0             # Code formatting
flake8>=6.0.0             # Linting
```

---

## 🔄 API Reference

### Pipeline API

#### `process(text: str) -> Dict`

Process a medical transcript through the full pipeline.

**Parameters:**
- `text` (str): Raw transcript text

**Returns:**
- `Dict`: Complete analysis results

**Raises:**
- `ValueError`: If text is empty
- `RuntimeError`: If processing fails

**Example:**
```python
result = pipeline.process(transcript)
```

#### `save_output(output: Dict, filename: str = None) -> str`

Save pipeline output to JSON file.

**Parameters:**
- `output` (Dict): Pipeline output dictionary
- `filename` (str, optional): Output filename

**Returns:**
- `str`: Path to saved file

**Example:**
```python
path = pipeline.save_output(result, 'analysis.json')
```

