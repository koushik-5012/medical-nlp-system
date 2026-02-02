"""
Speaker diarization module for medical transcripts.

This module separates doctor and patient dialogue from medical
transcription text into structured format.

Author: Koushik
Date: February 2026
"""

import re
from typing import List, Dict, Optional

from src.preprocessing.text_cleaner import TextCleaner


# ============================================================================
# SPEAKER DIARIZER CLASS
# ============================================================================
class SpeakerDiarizer:
    """
    Separate and structure doctor-patient dialogue.
    
    This class identifies speaker turns in medical transcripts and
    structures them into a list of dialogue dictionaries.
    
    Attributes:
        text_cleaner: TextCleaner instance for cleaning statements
        speaker_pattern: Regex pattern for identifying speakers
    
    Example:
        >>> diarizer = SpeakerDiarizer()
        >>> text = "Physician: Hello. Patient: Hi doctor."
        >>> dialogues = diarizer.parse_transcript(text)
        >>> print(dialogues[0])
        {'speaker': 'doctor', 'text': 'Hello.'}
    """
    
    def __init__(self):
        """Initialize the speaker diarizer."""
        # Text cleaner for cleaning individual statements
        self.text_cleaner = TextCleaner()
        
        # Pattern to match speaker labels
        # Matches: Physician:, Patient:, Doctor:, etc.
        self.speaker_pattern = re.compile(
            r'^(Physician|Patient|Doctor|Dr\.?|Pt\.?)[\s:]+',
            re.IGNORECASE | re.MULTILINE
        )
        
        # Speaker name mappings
        self.speaker_mappings = {
            'physician': 'doctor',
            'doctor': 'doctor',
            'dr': 'doctor',
            'patient': 'patient',
            'pt': 'patient',
        }
    def parse_transcript(self, text: str) -> List[Dict[str, str]]:
        """
        Parse transcript into structured dialogue list.
        
        Args:
            text: Raw transcript text with speaker labels
            
        Returns:
            List of dialogue dictionaries with 'speaker' and 'text' keys
            
        Example:
            >>> diarizer = SpeakerDiarizer()
            >>> result = diarizer.parse_transcript("Doctor: Hello\\nPatient: Hi")
            >>> len(result)
            2
        """
        if not text or not text.strip():
            return []
        
        dialogues = []
        lines = text.split('\n')
        
        current_speaker = None
        current_text = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip stage directions (text in brackets)
            if line.startswith('[') and line.endswith(']'):
                continue
            
            # Check if line starts with speaker label
            speaker_match = self.speaker_pattern.match(line)
            
            if speaker_match:
                # Save previous speaker's dialogue
                if current_speaker and current_text:
                    dialogues.append({
                        'speaker': current_speaker,
                        'text': self.text_cleaner.clean(' '.join(current_text))
                    })
                
                # Start new speaker turn
                speaker_label = speaker_match.group(1).lower().rstrip('.:')
                current_speaker = self._normalize_speaker(speaker_label)
                
                # Get text after speaker label
                text_after_label = line[speaker_match.end():].strip()
                current_text = [text_after_label] if text_after_label else []
            else:
                # Continuation of current speaker's text
                if current_speaker:
                    current_text.append(line)
        
        # Don't forget the last dialogue
        if current_speaker and current_text:
            dialogues.append({
                'speaker': current_speaker,
                'text': self.text_cleaner.clean(' '.join(current_text))
            })
        
        return dialogues
    def _normalize_speaker(self, speaker_label: str) -> str:
        """
        Normalize speaker labels to standard format.
        
        Args:
            speaker_label: Raw speaker label from transcript
            
        Returns:
            Normalized speaker name ('doctor' or 'patient')
        """
        # Remove common punctuation
        speaker_label = speaker_label.lower().strip().rstrip('.:')
        
        # Map to standard name
        return self.speaker_mappings.get(speaker_label, speaker_label)
    def get_patient_statements(self, dialogues: List[Dict[str, str]]) -> List[str]:
        """
        Extract only patient statements from dialogue list.
        
        Args:
            dialogues: List of dialogue dictionaries
            
        Returns:
            List of patient statements (text only)
        """
        return [
            d['text'] for d in dialogues 
            if d['speaker'] == 'patient' and d['text'].strip()
        ]
    
    def get_doctor_statements(self, dialogues: List[Dict[str, str]]) -> List[str]:
        """
        Extract only doctor statements from dialogue list.
        
        Args:
            dialogues: List of dialogue dictionaries
            
        Returns:
            List of doctor statements (text only)
        """
        return [
            d['text'] for d in dialogues 
            if d['speaker'] == 'doctor' and d['text'].strip()
        ]
    
    def get_dialogue_by_speaker(
        self, 
        dialogues: List[Dict[str, str]], 
        speaker: str
    ) -> List[Dict[str, str]]:
        """
        Filter dialogues by specific speaker.
        
        Args:
            dialogues: List of dialogue dictionaries
            speaker: Speaker to filter ('doctor' or 'patient')
            
        Returns:
            Filtered list of dialogue dictionaries
        """
        return [d for d in dialogues if d['speaker'] == speaker]
    def get_dialogue_stats(self, dialogues: List[Dict[str, str]]) -> Dict:
        """
        Get statistics about the dialogue.
        
        Args:
            dialogues: List of dialogue dictionaries
            
        Returns:
            Dictionary with dialogue statistics
        """
        if not dialogues:
            return {
                'total_turns': 0,
                'doctor_turns': 0,
                'patient_turns': 0,
                'total_words': 0,
            }
        
        doctor_turns = sum(1 for d in dialogues if d['speaker'] == 'doctor')
        patient_turns = sum(1 for d in dialogues if d['speaker'] == 'patient')
        
        total_words = sum(len(d['text'].split()) for d in dialogues)
        
        return {
            'total_turns': len(dialogues),
            'doctor_turns': doctor_turns,
            'patient_turns': patient_turns,
            'total_words': total_words,
            'avg_words_per_turn': total_words / len(dialogues) if dialogues else 0,
        }
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    """Quick test of SpeakerDiarizer functionality."""
    
    # Sample transcript
    test_transcript = """
    Physician: Good morning, Ms. Jones. How are you feeling today?
    
    Patient: Good morning, doctor. I'm doing better, but I still have 
    some discomfort now and then.
    
    Physician: I understand you were in a car accident last September.
    
    Patient: Yes, it was on September 1st. I was driving from Cheadle 
    Hulme to Manchester when another car hit me from behind.
    
    [Physical Examination Conducted]
    
    Physician: Everything looks good. Your neck and back have a full 
    range of movement.
    
    Patient: That's a relief!
    """
    
    # Initialize diarizer
    diarizer = SpeakerDiarizer()
    
    # Parse transcript
    dialogues = diarizer.parse_transcript(test_transcript)
    
    # Get statistics
    stats = diarizer.get_dialogue_stats(dialogues)
    
    # Get patient statements
    patient_statements = diarizer.get_patient_statements(dialogues)
    
    # Display results
    print("=" * 60)
    print("SPEAKER DIARIZATION TEST")
    print("=" * 60)
    
    print(f"\n📊 Statistics:")
    print(f"   Total turns: {stats['total_turns']}")
    print(f"   Doctor turns: {stats['doctor_turns']}")
    print(f"   Patient turns: {stats['patient_turns']}")
    print(f"   Total words: {stats['total_words']}")
    print(f"   Avg words/turn: {stats['avg_words_per_turn']:.1f}")
    
    print(f"\n💬 Parsed Dialogues:")
    for i, dialogue in enumerate(dialogues, 1):
        speaker_icon = "👨‍⚕️" if dialogue['speaker'] == 'doctor' else "🧑‍🦱"
        print(f"\n{i}. {speaker_icon} {dialogue['speaker'].upper()}:")
        print(f"   {dialogue['text'][:80]}..." if len(dialogue['text']) > 80 else f"   {dialogue['text']}")
    
    print(f"\n🧑‍🦱 Patient Statements Only ({len(patient_statements)}):")
    for i, stmt in enumerate(patient_statements, 1):
        preview = stmt[:60] + "..." if len(stmt) > 60 else stmt
        print(f"   {i}. {preview}")
    
    print("\n" + "=" * 60)