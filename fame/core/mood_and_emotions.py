from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class MoodAndEmotions:
    current_mood: str = "neutral"
    mood_intensity: float = 0.5
    emotional_state: List[str] = field(default_factory=list)
    raw_description: str = ""

    def __init__(self, description: str):
        """Initialize mood and emotions from description."""
        self.raw_description = description
        self.emotional_state = []
        self._parse_description()

    def _parse_description(self):
        """Parse the description to extract mood and emotions."""
        description = self.raw_description.lower()

        # Define mood keywords and their associated intensities
        mood_keywords = {
            "excited": (0.8, ["excited", "thrilled", "enthusiastic", "energetic"]),
            "happy": (0.7, ["happy", "joyful", "pleased", "delighted"]),
            "optimistic": (0.6, ["optimistic", "hopeful", "positive", "confident"]),
            "calm": (0.5, ["calm", "peaceful", "relaxed", "serene"]),
            "neutral": (0.5, ["neutral", "balanced", "steady", "composed"]),
            "thoughtful": (0.4, ["thoughtful", "contemplative", "reflective"]),
            "serious": (0.3, ["serious", "focused", "determined", "resolute"]),
            "concerned": (0.2, ["concerned", "worried", "anxious", "uneasy"]),
        }

        # Find the most relevant mood
        max_matches = 0
        best_mood = "neutral"
        best_intensity = 0.5

        for mood, (intensity, keywords) in mood_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in description)
            if matches > max_matches:
                max_matches = matches
                best_mood = mood
                best_intensity = intensity

        self.current_mood = best_mood
        self.mood_intensity = best_intensity

        # Extract emotional states
        emotional_keywords = {
            "passionate": ["passionate", "zealous", "ardent"],
            "curious": ["curious", "inquisitive", "interested"],
            "patient": ["patient", "understanding", "tolerant"],
            "encouraging": ["encouraging", "supportive", "motivating"],
            "analytical": ["analytical", "logical", "methodical"],
            "creative": ["creative", "innovative", "imaginative"],
            "friendly": ["friendly", "approachable", "welcoming"],
            "professional": ["professional", "formal", "composed"],
        }

        for emotion, keywords in emotional_keywords.items():
            if any(keyword in description for keyword in keywords):
                self.emotional_state.append(emotion)

    def get_mood_context(self) -> Dict[str, Any]:
        """Get comprehensive mood context."""
        return {
            "current_mood": self.current_mood,
            "mood_intensity": self.mood_intensity,
            "emotional_state": self.emotional_state,
        }

    def update_mood(self, new_mood: str, intensity: float = None):
        """Update the current mood and optionally its intensity."""
        self.current_mood = new_mood
        if intensity is not None:
            self.mood_intensity = max(0.0, min(1.0, intensity))
