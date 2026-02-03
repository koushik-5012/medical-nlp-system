"""
Main NLP pipeline orchestrator for medical transcripts.

This module connects all NLP components and runs them
in sequence to produce structured output from raw text.

Author: Koushik
Date: February 2026
"""

import json
import warnings
from typing import Dict, List, Optional
from datetime import datetime

from src.preprocessing import TextCleaner, SpeakerDiarizer, TemporalExtractor
from src.models.ner import ScispaCyNER, EntityValidator
from src.models.sentiment import SentimentAnalyzer
from src.models.intent import IntentClassifier
from src.models.summarization import MedicalKeywordExtractor, MedicalSummarizer
from src.config import OUTPUT_CONFIG, DATA_OUTPUT

warnings.filterwarnings('ignore')


class MedicalNLPPipeline:
    """
    Main pipeline that connects all NLP components.

    Takes a raw medical transcript as input and produces
    structured JSON output with entities, sentiment, intent,
    summary, and keywords.

    Example:
        >>> pipeline = MedicalNLPPipeline()
        >>> result = pipeline.process(open("transcript.txt").read())
        >>> print(result['summary']['diagnosis'])
    """

    def __init__(self):
        """Initialize all NLP components."""
        print("Loading pipeline components...")
        self.text_cleaner = TextCleaner()
        self.diarizer = SpeakerDiarizer()
        self.temporal_extractor = TemporalExtractor()
        self.ner = ScispaCyNER()
        self.entity_validator = EntityValidator()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.intent_classifier = IntentClassifier()
        self.keyword_extractor = MedicalKeywordExtractor()
        self.summarizer = MedicalSummarizer()
        print("✅ All components loaded!")

    def process(self, raw_text: str) -> Dict:
        """
        Run full pipeline on raw transcript.

        Args:
            raw_text: Raw medical transcript text

        Returns:
            Complete structured output dictionary
        """
        if not raw_text or not raw_text.strip():
            return {"error": "Empty input text"}

        print("\n🔄 Processing transcript...")

        print("   [1/7] Cleaning text...")
        cleaned_text = self.text_cleaner.clean(raw_text)

        print("   [2/7] Parsing speakers...")
        dialogues = self.diarizer.parse_transcript(raw_text)
        patient_statements = self.diarizer.get_patient_statements(dialogues)
        doctor_statements = self.diarizer.get_doctor_statements(dialogues)
        dialogue_stats = self.diarizer.get_dialogue_stats(dialogues)

        print("   [3/7] Extracting entities...")
        entities = self.ner.extract_entities(cleaned_text)
        entities = self.entity_validator.validate_entities_dict(entities)
        diagnosis = self.ner.extract_diagnosis(cleaned_text)
        prognosis = self.ner.extract_prognosis(cleaned_text)

        print("   [4/7] Extracting temporal info...")
        temporal = self.temporal_extractor.extract_all_temporal(cleaned_text)

        print("   [5/7] Analyzing sentiment...")
        sentiment_results = self.sentiment_analyzer.analyze_patient_statements(patient_statements)
        overall_sentiment = self.sentiment_analyzer.get_overall_sentiment(sentiment_results)
        sentiment_timeline = self.sentiment_analyzer.get_sentiment_timeline(sentiment_results)

        print("   [6/7] Classifying intents...")
        intent_results = self.intent_classifier.classify_patient_intents(patient_statements)
        intent_distribution = self.intent_classifier.get_intent_distribution(intent_results)

        print("   [7/7] Generating summary...")
        keywords = self.keyword_extractor.extract_keywords(cleaned_text)
        medical_phrases = self.keyword_extractor.extract_medical_phrases(cleaned_text)
        summary = self.summarizer.generate_summary(cleaned_text, dialogues)

        output = {
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "pipeline_version": "1.0.0",
                "total_dialogues": dialogue_stats['total_turns'],
                "doctor_turns": dialogue_stats['doctor_turns'],
                "patient_turns": dialogue_stats['patient_turns'],
            },
            "summary": {
                "patient_name": summary['patient_name'],
                "symptoms": summary['symptoms'],
                "diagnosis": diagnosis,
                "treatments": summary['treatments'],
                "current_status": summary['current_status'],
                "prognosis": prognosis,
            },
            "entities": entities,
            "temporal_info": {
                "dates": [d['text'] for d in temporal.get('dates', [])],
                "times": [t['text'] for t in temporal.get('times', [])],
                "durations": [d['text'] for d in temporal.get('durations', [])],
            },
            "sentiment_analysis": {
                "overall": overall_sentiment,
                "timeline": sentiment_timeline,
                "per_statement": sentiment_results,
            },
            "intent_analysis": {
                "distribution": intent_distribution,
                "per_statement": intent_results,
            },
            "keywords": {
                "top_keywords": [{"keyword": kw, "score": round(score, 3)} for kw, score in keywords],
                "medical_phrases": medical_phrases,
            },
            "dialogues": dialogues,
        }

        print("✅ Processing complete!\n")
        return output

    def save_output(self, output: Dict, filename: str = None) -> str:
        """
        Save pipeline output to JSON file.

        Args:
            output: Pipeline output dictionary
            filename: Output filename (auto-generated if None)

        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pipeline_output_{timestamp}.json"

        output_path = DATA_OUTPUT / filename

        with open(output_path, 'w') as f:
            json.dump(output, f, indent=OUTPUT_CONFIG['json_indent'], default=str)

        print(f"💾 Output saved to: {output_path}")
        return str(output_path)

    def load_transcript(self, filepath: str) -> str:
        """
        Load transcript from file.

        Args:
            filepath: Path to transcript file

        Returns:
            Transcript text
        """
        with open(filepath, 'r') as f:
            return f.read()


if __name__ == "__main__":
    """Test full pipeline with sample transcript."""

    pipeline = MedicalNLPPipeline()

    transcript_path = "data/raw/sample_transcript.txt"
    raw_text = pipeline.load_transcript(transcript_path)

    output = pipeline.process(raw_text)

    saved_path = pipeline.save_output(output)

    print("=" * 60)
    print("FULL PIPELINE TEST RESULTS")
    print("=" * 60)

    print(f"\n👤 Patient: {output['summary']['patient_name']}")
    print(f"🏥 Diagnosis: {output['summary']['diagnosis']}")
    print(f"📈 Prognosis: {output['summary']['prognosis']}")

    print(f"\n🔴 Symptoms:")
    for s in output['summary']['symptoms'][:5]:
        print(f"   • {s}")

    print(f"\n💊 Treatments:")
    for t in output['summary']['treatments'][:5]:
        print(f"   • {t}")

    print(f"\n😊 Sentiment:")
    print(f"   Dominant: {output['sentiment_analysis']['overall']['dominant_sentiment']}")
    print(f"   Distribution: {output['sentiment_analysis']['overall']['distribution']}")

    print(f"\n🎯 Top Intents:")
    for intent, count in sorted(output['intent_analysis']['distribution'].items(), key=lambda x: x[1], reverse=True)[:3]:
        if count > 0:
            print(f"   • {intent}: {count}")

    print(f"\n🔑 Medical Phrases:")
    for phrase in output['keywords']['medical_phrases'][:5]:
        print(f"   • {phrase}")

    print(f"\n📅 Temporal:")
    print(f"   Dates: {output['temporal_info']['dates']}")
    print(f"   Durations: {output['temporal_info']['durations']}")

    print(f"\n💾 Output saved to: {saved_path}")
    print("\n" + "=" * 60)
    print("✅ Full pipeline working correctly!")
    print("=" * 60)