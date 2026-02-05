# Testing Documentation

##  Test Suite Overview

The medical NLP system includes comprehensive unit tests to ensure reliability and correctness of all components.

### Test Coverage

| Module | Tests | Coverage |
|--------|-------|----------|
| NER | 3 tests | Core functionality |
| Pipeline | 2 tests | Integration |
| Preprocessing | Planned | Next iteration |
| Sentiment | Planned | Next iteration |

---

## 🚀 Running Tests

### Run All Tests
```bash
# Navigate to project root
cd ~/Desktop/medical-nlp-system

# Activate virtual environment
source venv/bin/activate

# Run all tests with verbose output
pytest tests/ -v
```

### Run Specific Test File
```bash
# Test NER module only
pytest tests/test_ner.py -v

# Test pipeline only
pytest tests/test_pipeline.py -v
```

### Run With Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html
```

---

## 📊 Sample Test Outputs

### Successful Test Run
```bash
$ pytest tests/ -v

======================== test session starts =========================
platform darwin -- Python 3.10.9, pytest-7.4.3
collected 5 items

tests/test_ner.py::test_ner_initialization PASSED            [ 20%]
tests/test_ner.py::test_extract_entities PASSED              [ 40%]
tests/test_ner.py::test_extract_diagnosis PASSED             [ 60%]
tests/test_pipeline.py::test_pipeline_initialization PASSED  [ 80%]
tests/test_pipeline.py::test_pipeline_process PASSED         [100%]

========================= 5 passed in 12.3s ==========================
```

### Detailed Test Output
```bash
$ pytest tests/test_ner.py -v -s

======================== test session starts =========================

tests/test_ner.py::test_ner_initialization 
✅ Loaded en_core_web_sm (fallback)
PASSED

tests/test_ner.py::test_extract_entities 
Testing entity extraction...
Entities found: {'symptoms': ['neck pain'], 'treatments': ['physiotherapy']}
PASSED

tests/test_ner.py::test_extract_diagnosis 
Testing diagnosis extraction...
Diagnosis: whiplash injury
PASSED

========================= 3 passed in 8.2s ===========================
```

### Failed Test Example
```bash
$ pytest tests/test_ner.py::test_extract_diagnosis -v

======================== test session starts =========================

tests/test_ner.py::test_extract_diagnosis FAILED             [100%]

============================== FAILURES ==============================
__________________ test_extract_diagnosis __________________________

    def test_extract_diagnosis():
        ner = ScispaCyNER()
        text = "Patient was diagnosed with whiplash injury"
        diagnosis = ner.extract_diagnosis(text)
        
>       assert diagnosis is not None
E       AssertionError: assert None is not None

tests/test_ner.py:25: AssertionError
======================== 1 failed in 2.1s ===========================
```

---

## 📝 Test Specifications

### test_ner.py

#### `test_ner_initialization()`

**Purpose:** Verify NER module initializes correctly

**Assertions:**
- NER object is created
- spaCy model is loaded
- nlp attribute is not None

**Expected Output:**
```
✅ Loaded en_core_web_sm (fallback)
PASSED
```

---

#### `test_extract_entities()`

**Purpose:** Verify entity extraction works

**Test Input:**
```
"Patient has neck pain and received physiotherapy"
```

**Assertions:**
- Entities dict contains 'symptoms' key
- Entities dict contains 'treatments' key
- At least one symptom is extracted

**Expected Entities:**
```python
{
  'symptoms': ['neck pain', 'pain'],
  'treatments': ['physiotherapy'],
  'diagnoses': [],
  'anatomy': ['neck']
}
```

---

#### `test_extract_diagnosis()`

**Purpose:** Verify diagnosis extraction

**Test Input:**
```
"Patient was diagnosed with whiplash injury"
```

**Assertions:**
- Diagnosis is not None
- 'whiplash' appears in diagnosis

**Expected Output:**
```
"whiplash injury"
```

---

### test_pipeline.py

#### `test_pipeline_initialization()`

**Purpose:** Verify pipeline initializes all components

**Assertions:**
- Pipeline object is created
- NER component is initialized
- Sentiment analyzer is initialized
- Intent classifier is initialized

**Expected Output:**
```
Loading pipeline components...
✅ All components loaded!
PASSED
```

---

#### `test_pipeline_process()`

**Purpose:** Verify end-to-end processing

**Test Input:**
```
"Patient: I have neck pain. Doctor: I see."
```

**Assertions:**
- Output contains 'entities' key
- Output contains 'sentiment_analysis' key
- Output contains 'summary' key
- Processing completes without errors

**Expected Output Structure:**
```python
{
  'entities': {...},
  'sentiment_analysis': {...},
  'intent_analysis': {...},
  'summary': {...},
  'metadata': {...}
}
```

---

##  Writing New Tests

### Test Template
```python
import pytest
from src.models.your_module import YourClass

def test_your_function():
    """
    Test description goes here.
    """
    # Arrange
    obj = YourClass()
    test_input = "..."
    
    # Act
    result = obj.your_method(test_input)
    
    # Assert
    assert result is not None
    assert 'expected_key' in result
    assert result['expected_key'] == "expected_value"

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
```

### Best Practices

1. **One assertion per test** (when possible)
2. **Clear test names** describing what is tested
3. **Arrange-Act-Assert** pattern
4. **Independent tests** (no dependencies between tests)
5. **Meaningful test data** (realistic examples)

---

## 🐛 Debugging Failed Tests

### Enable Verbose Output
```bash
pytest tests/test_ner.py -v -s
```

### Run Single Test
```bash
pytest tests/test_ner.py::test_extract_entities -v
```

### Print Debug Information

Add print statements in tests:
```python
def test_extract_entities():
    ner = ScispaCyNER()
    text = "Patient has neck pain"
    entities = ner.extract_entities(text)
    
    print(f"DEBUG: Entities = {entities}")  # Debug output
    
    assert len(entities['symptoms']) > 0
```

---

## 📈 Continuous Integration

### GitHub Actions Setup (Future)
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python -m spacy download en_core_web_sm
      - name: Run tests
        run: pytest tests/ -v
```

---

## ✅ Test Checklist

Before deployment, ensure:

- [ ] All tests pass locally
- [ ] No warnings in test output
- [ ] Coverage > 70% (when fully implemented)
- [ ] Tests run in < 30 seconds
- [ ] No hardcoded paths or credentials




