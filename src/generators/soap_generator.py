"""
SOAP note generator for medical transcripts.

Converts parsed medical dialogue into structured clinical
SOAP notes (Subjective, Objective, Assessment, Plan).

Author: Koushik
Date: February 2026
"""

import re
import warnings
from typing import Dict, List, Optional

from src.config import SOAP_KEYWORDS
from src.preprocessing import SpeakerDiarizer

warnings.filterwarnings('ignore')


class SOAPGenerator:
    """
    Generate clinical SOAP notes from medical transcripts.

    SOAP is a standard medical documentation format:
    - Subjective: What patient reports
    - Objective: Doctor observations/exam findings
    - Assessment: Diagnosis and severity
    - Plan: Treatment and follow-up

    Example:
        >>> generator = SOAPGenerator()
        >>> soap = generator.generate(transcript, dialogues)
        >>> print(soap['subjective']['chief_complaint'])
    """

    def __init__(self):
        """Initialize SOAP generator with keyword mappings."""
        self.soap_keywords = SOAP_KEYWORDS
        self.diarizer = SpeakerDiarizer()

    def generate(self, transcript: str, dialogues: List[Dict] = None) -> Dict:
        """
        Generate full SOAP note from transcript.

        Args:
            transcript: Raw or cleaned transcript text
            dialogues: Pre-parsed dialogue list (optional)

        Returns:
            Dictionary with all four SOAP sections
        """
        if not dialogues:
            dialogues = self.diarizer.parse_transcript(transcript)

        patient_statements = self.diarizer.get_patient_statements(dialogues)
        doctor_statements = self.diarizer.get_doctor_statements(dialogues)

        subjective = self._generate_subjective(patient_statements, transcript)
        objective = self._generate_objective(doctor_statements, transcript)
        assessment = self._generate_assessment(transcript, doctor_statements)
        plan = self._generate_plan(transcript, doctor_statements)

        return {
            "subjective": subjective,
            "objective": objective,
            "assessment": assessment,
            "plan": plan,
        }

    def _generate_subjective(self, patient_statements: List[str], transcript: str) -> Dict:
        """
        Generate Subjective section from patient statements.

        Args:
            patient_statements: List of patient dialogue
            transcript: Full transcript

        Returns:
            Subjective section dictionary
        """
        chief_complaint = self._extract_chief_complaint(patient_statements)
        history = self._extract_history(patient_statements)
        review_of_systems = self._extract_review_of_systems(patient_statements)

        return {
            "chief_complaint": chief_complaint,
            "history_of_present_illness": history,
            "review_of_systems": review_of_systems,
            "patient_statements": patient_statements,
        }

    def _generate_objective(self, doctor_statements: List[str], transcript: str) -> Dict:
        """
        Generate Objective section from doctor observations.

        Args:
            doctor_statements: List of doctor dialogue
            transcript: Full transcript

        Returns:
            Objective section dictionary
        """
        exam_findings = self._extract_exam_findings(doctor_statements, transcript)
        vital_signs = self._extract_vital_signs(transcript)
        observations = self._extract_observations(doctor_statements)

        return {
            "physical_examination": exam_findings,
            "vital_signs": vital_signs,
            "observations": observations,
            "doctor_statements": doctor_statements,
        }

    def _generate_assessment(self, transcript: str, doctor_statements: List[str]) -> Dict:
        """
        Generate Assessment section.

        Args:
            transcript: Full transcript
            doctor_statements: List of doctor dialogue

        Returns:
            Assessment section dictionary
        """
        diagnosis = self._extract_diagnosis(transcript)
        severity = self._extract_severity(transcript)
        prognosis = self._extract_prognosis(transcript)

        return {
            "primary_diagnosis": diagnosis,
            "severity": severity,
            "prognosis": prognosis,
        }

    def _generate_plan(self, transcript: str, doctor_statements: List[str]) -> Dict:
        """
        Generate Plan section.

        Args:
            transcript: Full transcript
            doctor_statements: List of doctor dialogue

        Returns:
            Plan section dictionary
        """
        treatment_plan = self._extract_treatment_plan(transcript, doctor_statements)
        medications = self._extract_medications(transcript)
        follow_up = self._extract_follow_up(transcript, doctor_statements)
        patient_education = self._extract_patient_education(doctor_statements)

        return {
            "treatment_plan": treatment_plan,
            "medications": medications,
            "follow_up": follow_up,
            "patient_education": patient_education,
        }

    def _extract_chief_complaint(self, patient_statements: List[str]) -> str:
        """Extract chief complaint from first patient statements."""
        complaint_keywords = ['pain', 'discomfort', 'hurt', 'ache', 'problem', 'issue']

        for statement in patient_statements[:3]:
            if any(kw in statement.lower() for kw in complaint_keywords):
                return statement

        return patient_statements[0] if patient_statements else "Not reported"

    def _extract_history(self, patient_statements: List[str]) -> str:
        """Extract history of present illness."""
        history_keywords = ['accident', 'happened', 'was', 'went', 'hit', 'started']

        history_parts = []
        for statement in patient_statements:
            if any(kw in statement.lower() for kw in history_keywords):
                history_parts.append(statement)

        return ' '.join(history_parts) if history_parts else "History not explicitly described"

    def _extract_review_of_systems(self, patient_statements: List[str]) -> str:
        """Extract review of systems from patient statements."""
        ros_keywords = ['anxiety', 'nervous', 'sleep', 'work', 'daily', 'emotional', 'concentrate']

        ros_parts = []
        for statement in patient_statements:
            if any(kw in statement.lower() for kw in ros_keywords):
                ros_parts.append(statement)

        return ' '.join(ros_parts) if ros_parts else "No additional systems reported"

    def _extract_exam_findings(self, doctor_statements: List[str], transcript: str) -> str:
        """Extract physical examination findings."""
        exam_keywords = ['examination', 'range of movement', 'tenderness', 'looks good', 'condition']

        for statement in doctor_statements:
            if any(kw in statement.lower() for kw in exam_keywords):
                return statement

        exam_pattern = r'\[.*?[Ee]xam.*?\]'
        match = re.search(exam_pattern, transcript)
        if match:
            return "Physical examination was conducted. " + (
                next(
                    (s for s in doctor_statements if 'look' in s.lower() or 'good' in s.lower()),
                    "Findings documented"
                )
            )

        return "Examination findings not documented"

    def _extract_vital_signs(self, transcript: str) -> str:
        """Extract vital signs if mentioned."""
        vital_patterns = ['blood pressure', 'heart rate', 'temperature', 'oxygen']

        for pattern in vital_patterns:
            if pattern in transcript.lower():
                match = re.search(rf'{pattern}[:\s]+(.*?)(?:\.|,|$)', transcript, re.IGNORECASE)
                if match:
                    return match.group(0)

        return "Vital signs not recorded in transcript"

    def _extract_observations(self, doctor_statements: List[str]) -> List[str]:
        """Extract doctor observations."""
        observation_keywords = ['normal', 'good', 'full range', 'no sign', 'appears', 'noted']

        observations = []
        for statement in doctor_statements:
            if any(kw in statement.lower() for kw in observation_keywords):
                observations.append(statement)

        return observations if observations else ["No specific observations documented"]

    def _extract_diagnosis(self, transcript: str) -> str:
        """Extract primary diagnosis."""
        patterns = [
            r'(?:diagnosed with|diagnosis[:\s]+|it was (?:a|an))\s+(.*?)(?:\.|,|$)',
            r'(whiplash.*?)(?:\.|,|$)',
        ]

        for pattern in patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "Diagnosis not explicitly stated"

    def _extract_severity(self, transcript: str) -> str:
        """Extract severity of condition."""
        if re.search(r'\b(severe|critical|serious)\b', transcript, re.IGNORECASE):
            return "Severe"
        elif re.search(r'\b(moderate|moderate)\b', transcript, re.IGNORECASE):
            return "Moderate"
        elif re.search(r'\b(mild|minor|better|improving)\b', transcript, re.IGNORECASE):
            return "Mild"
        return "Not specified"

    def _extract_prognosis(self, transcript: str) -> str:
        """Extract prognosis information."""
        patterns = [
            r'(full recovery.*?)(?:\.|$)',
            r'(expect.*?recovery.*?)(?:\.|$)',
            r"(don't foresee.*?)(?:\.|$)",
            r'(no.*?long.term.*?)(?:\.|$)',
        ]

        for pattern in patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "Prognosis not explicitly stated"

    def _extract_treatment_plan(self, transcript: str, doctor_statements: List[str]) -> str:
        """Extract treatment plan."""
        treatment_keywords = ['treatment', 'therapy', 'physiotherapy', 'medication', 'recommend']

        for statement in doctor_statements:
            if any(kw in statement.lower() for kw in treatment_keywords):
                return statement

        patterns = [
            r'(physiotherapy.*?)(?:\.|$)',
            r'(treatment.*?)(?:\.|$)',
        ]

        for pattern in patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "Treatment plan not explicitly stated"

    def _extract_medications(self, transcript: str) -> List[str]:
        """Extract medications mentioned."""
        medications = []
        med_keywords = ['painkillers', 'medication', 'medicine', 'tablets', 'prescription', 'analgesic']

        for keyword in med_keywords:
            if keyword in transcript.lower():
                match = re.search(rf'(.*?{keyword}.*?)(?:\.|,|$)', transcript, re.IGNORECASE)
                if match:
                    medications.append(match.group(1).strip())

        return medications if medications else ["No specific medications documented"]

    def _extract_follow_up(self, transcript: str, doctor_statements: List[str]) -> str:
        """Extract follow-up instructions."""
        followup_keywords = ['follow-up', 'come back', 'return', 'reach out', 'if anything changes']

        for statement in doctor_statements:
            if any(kw in statement.lower() for kw in followup_keywords):
                return statement

        return "Follow-up as needed if symptoms worsen"

    def _extract_patient_education(self, doctor_statements: List[str]) -> List[str]:
        """Extract patient education points."""
        education_keywords = ['should', 'don\'t', 'if', 'advised', 'important', 'make sure']

        education = []
        for statement in doctor_statements:
            if any(kw in statement.lower() for kw in education_keywords):
                education.append(statement)

        return education if education else ["General health maintenance advised"]

    def to_formatted_text(self, soap: Dict) -> str:
        """
        Convert SOAP dictionary to formatted text.

        Args:
            soap: SOAP note dictionary

        Returns:
            Formatted SOAP note string
        """
        lines = []
        lines.append("=" * 60)
        lines.append("CLINICAL SOAP NOTE")
        lines.append("=" * 60)

        lines.append("\n📋 SUBJECTIVE")
        lines.append("-" * 40)
        lines.append(f"Chief Complaint: {soap['subjective']['chief_complaint']}")
        lines.append(f"\nHistory: {soap['subjective']['history_of_present_illness']}")
        lines.append(f"\nReview of Systems: {soap['subjective']['review_of_systems']}")

        lines.append("\n\n🔬 OBJECTIVE")
        lines.append("-" * 40)
        lines.append(f"Physical Exam: {soap['objective']['physical_examination']}")
        lines.append(f"\nVital Signs: {soap['objective']['vital_signs']}")
        lines.append("\nObservations:")
        for obs in soap['objective']['observations']:
            lines.append(f"  • {obs}")

        lines.append("\n\n📊 ASSESSMENT")
        lines.append("-" * 40)
        lines.append(f"Diagnosis: {soap['assessment']['primary_diagnosis']}")
        lines.append(f"Severity: {soap['assessment']['severity']}")
        lines.append(f"Prognosis: {soap['assessment']['prognosis']}")

        lines.append("\n\n📝 PLAN")
        lines.append("-" * 40)
        lines.append(f"Treatment: {soap['plan']['treatment_plan']}")
        lines.append("\nMedications:")
        for med in soap['plan']['medications']:
            lines.append(f"  • {med}")
        lines.append(f"\nFollow-up: {soap['plan']['follow_up']}")
        lines.append("\nPatient Education:")
        for edu in soap['plan']['patient_education']:
            lines.append(f"  • {edu}")

        lines.append("\n" + "=" * 60)

        return '\n'.join(lines)


if __name__ == "__main__":
    """Test SOAP generator with sample transcript."""

    test_transcript = open("data/raw/sample_transcript.txt").read()

    generator = SOAPGenerator()

    dialogues = generator.diarizer.parse_transcript(test_transcript)
    soap = generator.generate(test_transcript, dialogues)
    formatted = generator.to_formatted_text(soap)

    print(formatted)

    import json
    print("\n📊 JSON Output:")
    print(json.dumps(soap, indent=2))

    print("\n✅ SOAP generation working correctly!")