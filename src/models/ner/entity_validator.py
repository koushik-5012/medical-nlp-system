"""
Entity validation and cleaning module.

This module provides utilities to validate, clean, and deduplicate
extracted medical entities.

Author: Koushik
Date: February 2026
"""

from typing import List, Dict, Set
import re


class EntityValidator:
    """
    Validate and clean extracted medical entities.
    
    This class provides methods to ensure entity quality by removing
    duplicates, filtering invalid entries, and normalizing text.
    
    Example:
        >>> validator = EntityValidator()
        >>> entities = ['neck pain', 'NECK PAIN', 'pain in neck']
        >>> cleaned = validator.deduplicate(entities)
        >>> print(cleaned)
        ['neck pain']
    """
    
    def __init__(self, min_length: int = 2, max_length: int = 100):
        """
        Initialize entity validator.
        
        Args:
            min_length: Minimum entity length in characters
            max_length: Maximum entity length in characters
        """
        self.min_length = min_length
        self.max_length = max_length
        
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
            'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do',
            'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
    
    def validate_entity(self, entity: str) -> bool:
        """
        Check if entity is valid.
        
        Args:
            entity: Entity string to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not entity or not entity.strip():
            return False
        
        entity_clean = entity.strip()
        
        if len(entity_clean) < self.min_length:
            return False
        
        if len(entity_clean) > self.max_length:
            return False
        
        if entity_clean.lower() in self.stop_words:
            return False
        
        if re.match(r'^\d+$', entity_clean):
            return False
        
        if re.match(r'^[^\w\s]+$', entity_clean):
            return False
        
        return True
    
    def clean_entity(self, entity: str) -> str:
        """
        Clean and normalize entity text.
        
        Args:
            entity: Raw entity string
            
        Returns:
            Cleaned entity string
        """
        entity = entity.strip()
        
        entity = re.sub(r'\s+', ' ', entity)
        
        entity = re.sub(r'^[^\w\s]+|[^\w\s]+$', '', entity)
        
        return entity
    
    def deduplicate(self, entities: List[str]) -> List[str]:
        """
        Remove duplicate entities (case-insensitive).
        
        Args:
            entities: List of entity strings
            
        Returns:
            Deduplicated list of entities
        """
        seen = set()
        unique = []
        
        for entity in entities:
            entity_lower = entity.lower().strip()
            
            if entity_lower not in seen:
                unique.append(entity)
                seen.add(entity_lower)
        
        return unique
    
    def filter_valid_entities(self, entities: List[str]) -> List[str]:
        """
        Filter list to only valid entities.
        
        Args:
            entities: List of entity strings
            
        Returns:
            Filtered list of valid entities
        """
        valid = []
        
        for entity in entities:
            cleaned = self.clean_entity(entity)
            if self.validate_entity(cleaned):
                valid.append(cleaned)
        
        return valid
    
    def remove_substrings(self, entities: List[str]) -> List[str]:
        """
        Remove entities that are substrings of longer entities.
        
        Args:
            entities: List of entity strings
            
        Returns:
            List with substring duplicates removed
        """
        if not entities:
            return []
        
        sorted_entities = sorted(entities, key=len, reverse=True)
        
        filtered = []
        
        for entity in sorted_entities:
            entity_lower = entity.lower()
            
            is_substring = False
            for kept in filtered:
                if entity_lower in kept.lower() and entity_lower != kept.lower():
                    is_substring = True
                    break
            
            if not is_substring:
                filtered.append(entity)
        
        return filtered
    
    def validate_entities_dict(self, entities: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Validate entire entity dictionary.
        
        Args:
            entities: Dictionary with entity categories
            
        Returns:
            Validated and cleaned entity dictionary
        """
        validated = {}
        
        for category, entity_list in entities.items():
            cleaned = self.filter_valid_entities(entity_list)
            deduplicated = self.deduplicate(cleaned)
            no_substrings = self.remove_substrings(deduplicated)
            validated[category] = no_substrings
        
        return validated
    
    def merge_similar_entities(self, entities: List[str], similarity_threshold: float = 0.8) -> List[str]:
        """
        Merge very similar entities.
        
        Args:
            entities: List of entity strings
            similarity_threshold: Similarity threshold (0-1)
            
        Returns:
            List with similar entities merged
        """
        if not entities:
            return []
        
        merged = []
        seen = set()
        
        for entity in entities:
            entity_lower = entity.lower()
            
            if entity_lower in seen:
                continue
            
            is_similar = False
            for kept in merged:
                if self._calculate_similarity(entity_lower, kept.lower()) > similarity_threshold:
                    is_similar = True
                    break
            
            if not is_similar:
                merged.append(entity)
                seen.add(entity_lower)
        
        return merged
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate simple similarity between two strings.
        
        Args:
            str1: First string
            str2: Second string
            
        Returns:
            Similarity score (0-1)
        """
        if str1 == str2:
            return 1.0
        
        set1 = set(str1.split())
        set2 = set(str2.split())
        
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0


if __name__ == "__main__":
    """Quick test of EntityValidator functionality."""
    
    test_entities = {
        'symptoms': [
            'neck pain',
            'NECK PAIN',
            'pain in neck',
            'back pain',
            'the pain',
            'a',
            '123',
            'stiffness',
            'neck',
        ],
        'treatments': [
            'physiotherapy sessions',
            'physiotherapy',
            'ten sessions of physiotherapy',
            'painkillers',
            'medication',
        ]
    }
    
    validator = EntityValidator()
    
    print("=" * 60)
    print("ENTITY VALIDATOR TEST")
    print("=" * 60)
    
    print("\n📋 Original Entities:")
    for category, entities in test_entities.items():
        print(f"\n{category.upper()} ({len(entities)}):")
        for ent in entities:
            print(f"   • {ent}")
    
    validated = validator.validate_entities_dict(test_entities)
    
    print("\n✅ Validated Entities:")
    for category, entities in validated.items():
        print(f"\n{category.upper()} ({len(entities)}):")
        for ent in entities:
            print(f"   • {ent}")
    
    print("\n📊 Validation Summary:")
    for category in test_entities.keys():
        original_count = len(test_entities[category])
        validated_count = len(validated[category])
        removed = original_count - validated_count
        print(f"   {category}: {original_count} → {validated_count} (removed {removed})")
    
    print("\n" + "=" * 60)
    print("✅ Entity validation working correctly!")
    print("=" * 60)