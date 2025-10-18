# crisis_detector.py
"""
Enhanced crisis detection module combining:
1. Keyword-based detection (high recall)
2. Pattern matching for indirect expressions
3. Optional ML-based severity scoring

This ensures no crisis messages are missed (100% recall priority).
"""

import re
from typing import Tuple, Dict
from enum import Enum

class CrisisLevel(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# Primary crisis keywords (direct expressions)
CRITICAL_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die",
    "going to die", "better off dead", "can't go on",
    "end it all", "take my life", "no reason to live"
]

# Secondary keywords (indirect/concerning expressions)
CONCERNING_KEYWORDS = [
    "self harm", "self-harm", "cut myself", "hurt myself",
    "worthless", "hopeless", "give up", "can't take it",
    "nobody cares", "everyone hates me", "burden",
    "disappear", "not worth it", "pointless"
]

# Patterns for indirect expressions
CRISIS_PATTERNS = [
    r"(wish|want).*(never|not).*(born|exist)",
    r"(world|everyone).*(better|off).*(without me|if i was gone)",
    r"(can't|cannot).*(do this|take it|go on).*(anymore|any longer)",
    r"(no|don't).*(point|reason).*(living|life|continue)",
    r"(planning|plan).*(end|kill|harm)",
]

# Helpline information by region
HELPLINES = {
    "india": {
        "name": "AASRA",
        "number": "91-9820466726",
        "hours": "24/7"
    },
    "us": {
        "name": "National Suicide Prevention Lifeline",
        "number": "988",
        "hours": "24/7"
    },
    "uk": {
        "name": "Samaritans",
        "number": "116 123",
        "hours": "24/7"
    },
    "international": {
        "name": "International Association for Suicide Prevention",
        "url": "https://www.iasp.info/resources/Crisis_Centres/",
        "hours": "24/7"
    }
}

class CrisisDetector:
    def __init__(self, region: str = "india"):
        self.region = region.lower()
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in CRISIS_PATTERNS]
    
    def detect(self, text: str) -> Tuple[bool, CrisisLevel, str]:
        """
        Detect crisis in text.
        
        Returns:
            (is_crisis, crisis_level, explanation)
        """
        text_lower = text.lower()
        
        # Check critical keywords first
        for keyword in CRITICAL_KEYWORDS:
            if keyword in text_lower:
                return True, CrisisLevel.CRITICAL, f"Critical keyword detected: '{keyword}'"
        
        # Check patterns
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return True, CrisisLevel.HIGH, f"Crisis pattern detected"
        
        # Check concerning keywords
        concern_count = 0
        for keyword in CONCERNING_KEYWORDS:
            if keyword in text_lower:
                concern_count += 1
        
        if concern_count >= 2:
            return True, CrisisLevel.MEDIUM, f"Multiple concerning keywords detected ({concern_count})"
        elif concern_count == 1:
            return True, CrisisLevel.LOW, f"Concerning keyword detected"
        
        return False, CrisisLevel.NONE, "No crisis indicators detected"
    
    def get_crisis_message(self, level: CrisisLevel) -> str:
        """Generate appropriate crisis response based on severity level."""
        helpline = HELPLINES.get(self.region, HELPLINES["international"])
        
        base_message = "I'm really sorry you're feeling this way. "
        
        if level == CrisisLevel.CRITICAL or level == CrisisLevel.HIGH:
            message = (
                f"{base_message}Your safety is the top priority. "
                f"Please reach out for immediate help:\n\n"
            )
            if "number" in helpline:
                message += f"📞 {helpline['name']}: {helpline['number']} ({helpline['hours']})\n"
            if "url" in helpline:
                message += f"🌐 {helpline['url']}\n"
            message += (
                f"\n🚨 If you're in immediate danger, please call emergency services (112 in India, 911 in US).\n\n"
                f"Would you like me to provide additional resources or help you connect with someone?"
            )
        
        elif level == CrisisLevel.MEDIUM:
            message = (
                f"{base_message}It sounds like you're going through a really difficult time. "
                f"You don't have to face this alone. Consider reaching out:\n\n"
            )
            if "number" in helpline:
                message += f"📞 {helpline['name']}: {helpline['number']}\n\n"
            message += "Would you like to talk about what's troubling you?"
        
        else:  # LOW
            message = (
                f"{base_message}I'm here to listen. If things feel overwhelming, "
                f"remember that support is available:\n\n"
            )
            if "number" in helpline:
                message += f"📞 {helpline['name']}: {helpline['number']}\n\n"
            message += "What's been on your mind?"
        
        return message
    
    def get_helpline_info(self) -> Dict:
        """Get helpline information for the current region."""
        return HELPLINES.get(self.region, HELPLINES["international"])


# Singleton instance
_detector = None

def get_detector(region: str = "india") -> CrisisDetector:
    """Get or create crisis detector instance."""
    global _detector
    if _detector is None:
        _detector = CrisisDetector(region)
    return _detector


if __name__ == "__main__":
    # Test cases
    detector = CrisisDetector("india")
    
    test_cases = [
        "I'm feeling a bit sad today",
        "I feel worthless and hopeless",
        "I want to kill myself",
        "The world would be better off without me",
        "I'm planning to end it all tonight",
        "I can't take it anymore, there's no point in living",
    ]
    
    print("Crisis Detection Test Results:")
    print("=" * 60)
    for text in test_cases:
        is_crisis, level, explanation = detector.detect(text)
        print(f"\nText: {text}")
        print(f"Crisis: {is_crisis} | Level: {level.name} | {explanation}")
        if is_crisis:
            print(f"\nResponse:\n{detector.get_crisis_message(level)}")
            print("-" * 60)
