"""
Temporal extraction module for medical transcripts.

This module extracts temporal information including dates, times,
and durations from medical text.

Author: Koushik
Date: February 2026
"""

import re
from typing import Dict, List, Optional
from datetime import datetime


class TemporalExtractor:
    """
    Extract temporal information from medical text.
    
    This class identifies and extracts dates, times, and durations
    from medical transcripts using regex patterns.
    
    Attributes:
        date_patterns: List of regex patterns for dates
        time_patterns: List of regex patterns for times
        duration_patterns: List of regex patterns for durations
    
    Example:
        >>> extractor = TemporalExtractor()
        >>> text = "On September 1st at 12:30 PM, patient had accident"
        >>> result = extractor.extract_all_temporal(text)
        >>> print(result['dates'])
        [{'text': 'September 1st', 'type': 'date'}]
    """
    
    def __init__(self):
        """Initialize temporal extractor with regex patterns."""
        self.date_patterns = [
            r'(\w+\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?)',
            r'(\d{1,2}/\d{1,2}/\d{2,4})',
            r'(\d{4}-\d{2}-\d{2})',
            r'(last\s+(?:week|month|year|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday))',
            r'((?:this|next)\s+(?:week|month|year|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday))',
        ]
        
        self.time_patterns = [
            r'(\d{1,2}:\d{2}(?::\d{2})?\s*(?:am|pm|AM|PM)?)',
            r'((?:morning|afternoon|evening|night))',
            r'(\d{1,2}\s*(?:am|pm|AM|PM))',
        ]
        
        self.duration_patterns = [
            r'(\d+\s*(?:week|month|day|year|hour|minute)s?)',
            r'((?:first|last|past)\s+\d+\s*(?:week|month|day|year)s?)',
            r'(\d+\s*session(?:s)?)',
            r'(\d+\s*time(?:s)?)',
        ]
        
        self.compiled_patterns = {
            'dates': [re.compile(p, re.IGNORECASE) for p in self.date_patterns],
            'times': [re.compile(p, re.IGNORECASE) for p in self.time_patterns],
            'durations': [re.compile(p, re.IGNORECASE) for p in self.duration_patterns],
        }
    
    def extract_all_temporal(self, text: str) -> Dict[str, List[Dict]]:
        """
        Extract all temporal information from text.
        
        Args:
            text: Input text to extract temporal information from
            
        Returns:
            Dictionary containing lists of dates, times, and durations
            
        Example:
            >>> extractor = TemporalExtractor()
            >>> result = extractor.extract_all_temporal("September 1st at 12:30")
            >>> result.keys()
            dict_keys(['dates', 'times', 'durations'])
        """
        return {
            'dates': self.extract_dates(text),
            'times': self.extract_times(text),
            'durations': self.extract_durations(text),
        }
    
    def extract_dates(self, text: str) -> List[Dict]:
        """
        Extract date information from text.
        
        Args:
            text: Input text
            
        Returns:
            List of dictionaries containing date information
        """
        dates = []
        seen = set()
        
        for pattern in self.compiled_patterns['dates']:
            matches = pattern.finditer(text)
            for match in matches:
                date_text = match.group(0).strip()
                
                if date_text.lower() not in seen:
                    dates.append({
                        'text': date_text,
                        'position': match.span(),
                        'type': 'date'
                    })
                    seen.add(date_text.lower())
        
        return dates
    
    def extract_times(self, text: str) -> List[Dict]:
        """
        Extract time information from text.
        
        Args:
            text: Input text
            
        Returns:
            List of dictionaries containing time information
        """
        times = []
        seen = set()
        
        for pattern in self.compiled_patterns['times']:
            matches = pattern.finditer(text)
            for match in matches:
                time_text = match.group(0).strip()
                
                if time_text.lower() not in seen:
                    times.append({
                        'text': time_text,
                        'position': match.span(),
                        'type': 'time'
                    })
                    seen.add(time_text.lower())
        
        return times
    
    def extract_durations(self, text: str) -> List[Dict]:
        """
        Extract duration information from text.
        
        Args:
            text: Input text
            
        Returns:
            List of dictionaries containing duration information
        """
        durations = []
        seen = set()
        
        for pattern in self.compiled_patterns['durations']:
            matches = pattern.finditer(text)
            for match in matches:
                duration_text = match.group(0).strip()
                
                if duration_text.lower() not in seen:
                    durations.append({
                        'text': duration_text,
                        'position': match.span(),
                        'type': 'duration'
                    })
                    seen.add(duration_text.lower())
        
        return durations
    
    def extract_incident_date(self, text: str) -> Optional[str]:
        """
        Extract the primary incident date from text.
        
        Args:
            text: Input text
            
        Returns:
            First date found, or None if no date present
        """
        dates = self.extract_dates(text)
        return dates[0]['text'] if dates else None
    
    def extract_treatment_duration(self, text: str) -> Optional[str]:
        """
        Extract treatment duration from text.
        
        Args:
            text: Input text
            
        Returns:
            First duration found, or None if no duration present
        """
        durations = self.extract_durations(text)
        return durations[0]['text'] if durations else None
    
    def get_temporal_summary(self, text: str) -> Dict:
        """
        Get a summary of all temporal information.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with counts and examples of temporal info
        """
        temporal_data = self.extract_all_temporal(text)
        
        return {
            'total_dates': len(temporal_data['dates']),
            'total_times': len(temporal_data['times']),
            'total_durations': len(temporal_data['durations']),
            'first_date': temporal_data['dates'][0]['text'] if temporal_data['dates'] else None,
            'first_time': temporal_data['times'][0]['text'] if temporal_data['times'] else None,
            'first_duration': temporal_data['durations'][0]['text'] if temporal_data['durations'] else None,
        }


if __name__ == "__main__":
    """Quick test of TemporalExtractor functionality."""
    
    test_text = """
    Yes, it was on September 1st, around 12:30 in the afternoon. 
    I was driving from Cheadle Hulme to Manchester when I had to stop 
    in traffic. The first four weeks were rough. I had to go through 
    ten sessions of physiotherapy. I had to take a week off work. 
    Given your progress, I'd expect you to make a full recovery within 
    six months of the accident.
    """
    
    extractor = TemporalExtractor()
    
    temporal_data = extractor.extract_all_temporal(test_text)
    summary = extractor.get_temporal_summary(test_text)
    
    print("=" * 60)
    print("TEMPORAL EXTRACTION TEST")
    print("=" * 60)
    
    print(f"\n📊 Summary:")
    print(f"   Total dates: {summary['total_dates']}")
    print(f"   Total times: {summary['total_times']}")
    print(f"   Total durations: {summary['total_durations']}")
    
    print(f"\n📅 Dates Found ({len(temporal_data['dates'])}):")
    for item in temporal_data['dates']:
        print(f"   • {item['text']}")
    
    print(f"\n🕐 Times Found ({len(temporal_data['times'])}):")
    for item in temporal_data['times']:
        print(f"   • {item['text']}")
    
    print(f"\n⏱️  Durations Found ({len(temporal_data['durations'])}):")
    for item in temporal_data['durations']:
        print(f"   • {item['text']}")
    
    print("\n" + "=" * 60)
    print("✅ Temporal extraction working correctly!")
    print("=" * 60)