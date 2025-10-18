# tests/test_crisis_detector.py
"""
Unit tests for crisis detection module.
"""

import pytest
from crisis_detector import CrisisDetector, CrisisLevel, get_detector


class TestCrisisDetector:
    """Test suite for crisis detection functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.detector = CrisisDetector(region="india")
    
    def test_critical_keywords(self):
        """Test detection of critical crisis keywords."""
        test_cases = [
            "I want to kill myself",
            "I'm going to end my life",
            "suicide is the only option",
            "I want to die"
        ]
        
        for text in test_cases:
            is_crisis, level, _ = self.detector.detect(text)
            assert is_crisis is True, f"Failed to detect crisis in: {text}"
            assert level == CrisisLevel.CRITICAL, f"Wrong level for: {text}"
    
    def test_high_severity_patterns(self):
        """Test detection of high severity patterns."""
        test_cases = [
            "The world would be better without me",
            "I can't go on anymore, there's no point",
            "nobody would miss me if I was gone"
        ]
        
        for text in test_cases:
            is_crisis, level, _ = self.detector.detect(text)
            assert is_crisis is True, f"Failed to detect crisis in: {text}"
            assert level in [CrisisLevel.HIGH, CrisisLevel.CRITICAL], f"Wrong level for: {text}"
    
    def test_medium_severity(self):
        """Test detection of medium severity concerns."""
        test_cases = [
            "I feel worthless and hopeless",
            "I'm a burden to everyone, nobody cares",
            "I want to hurt myself"
        ]
        
        for text in test_cases:
            is_crisis, level, _ = self.detector.detect(text)
            assert is_crisis is True, f"Failed to detect crisis in: {text}"
            assert level in [CrisisLevel.MEDIUM, CrisisLevel.HIGH], f"Wrong level for: {text}"
    
    def test_non_crisis_messages(self):
        """Test that normal messages are not flagged as crisis."""
        test_cases = [
            "I'm feeling sad today",
            "I had a bad day at work",
            "I'm stressed about exams",
            "I feel lonely sometimes",
            "I'm tired of this situation"
        ]
        
        for text in test_cases:
            is_crisis, level, _ = self.detector.detect(text)
            assert is_crisis is False, f"False positive for: {text}"
            assert level == CrisisLevel.NONE, f"Wrong level for non-crisis: {text}"
    
    def test_helpline_message_generation(self):
        """Test that appropriate helpline messages are generated."""
        critical_text = "I want to kill myself"
        is_crisis, level, _ = self.detector.detect(critical_text)
        
        message = self.detector.get_crisis_message(level)
        
        assert "AASRA" in message or "helpline" in message.lower()
        assert "91-9820466726" in message or "emergency" in message.lower()
    
    def test_get_detector_singleton(self):
        """Test that get_detector returns consistent instance."""
        detector1 = get_detector("india")
        detector2 = get_detector("india")
        
        # Should return same instance
        assert detector1 is detector2
    
    def test_different_regions(self):
        """Test helpline info for different regions."""
        regions = ["india", "us", "uk", "international"]
        
        for region in regions:
            detector = CrisisDetector(region)
            helpline_info = detector.get_helpline_info()
            
            assert helpline_info is not None
            assert isinstance(helpline_info, dict)
    
    def test_case_insensitive_detection(self):
        """Test that detection is case-insensitive."""
        test_cases = [
            "I WANT TO KILL MYSELF",
            "i want to kill myself",
            "I Want To Kill Myself"
        ]
        
        for text in test_cases:
            is_crisis, level, _ = self.detector.detect(text)
            assert is_crisis is True
            assert level == CrisisLevel.CRITICAL
    
    def test_no_false_negatives(self):
        """Critical test: Ensure no crisis messages are missed."""
        # These MUST all be detected
        critical_cases = [
            "I want to end my life",
            "planning to kill myself tonight",
            "suicide seems like the only way out",
            "I'm going to die by suicide",
            "I want to take my own life"
        ]
        
        false_negatives = []
        for text in critical_cases:
            is_crisis, _, _ = self.detector.detect(text)
            if not is_crisis:
                false_negatives.append(text)
        
        assert len(false_negatives) == 0, f"CRITICAL: Missed crisis messages: {false_negatives}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
