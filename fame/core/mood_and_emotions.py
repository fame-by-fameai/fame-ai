from dataclasses import dataclass, field
from typing import Dict, Any
import random
from fame.utils.sentiment_analysis import SentimentAnalyzer


@dataclass
class MoodAndEmotions:
    current_mood: str = "neutral"
    mood_intensity: float = 0.5  # 0.0 to 1.0
    emotional_stability: float = 0.7  # 0.0 to 1.0
    emoji_style: Dict[str, Any] = field(
        default_factory=lambda: {
            "frequency": 0.5,  # 0.0 (never) to 1.0 (very frequent)
            "style": "cheerful",  # cheerful, professional, minimal, expressive
            "max_per_post": 2,
        }
    )
    raw_description: str = ""

    def __post_init__(self):
        """Initialize after dataclass fields are set."""
        self._parse_description()
        self._analyzer = SentimentAnalyzer()

    def _parse_description(self):
        """Parse the description to set mood and emotional parameters."""
        description = self.raw_description.lower()

        # Set emoji style based on personality indicators
        if any(word in description for word in ["professional", "formal", "serious"]):
            self.emoji_style.update(
                {
                    "frequency": 0.2,
                    "style": "professional",
                    "max_per_post": 1,
                }
            )
        elif any(
            word in description
            for word in ["cheerful", "playful", "fun", "social media"]
        ):
            self.emoji_style.update(
                {
                    "frequency": 0.8,
                    "style": "cheerful",
                    "max_per_post": 3,
                }
            )
        elif any(
            word in description for word in ["expressive", "artistic", "creative"]
        ):
            self.emoji_style.update(
                {
                    "frequency": 0.7,
                    "style": "expressive",
                    "max_per_post": 2,
                }
            )

        # Set mood intensity based on descriptive words
        intensity_words = {
            "very": 0.9,
            "extremely": 1.0,
            "somewhat": 0.4,
            "slightly": 0.3,
            "moderately": 0.6,
        }
        for word, value in intensity_words.items():
            if word in description:
                self.mood_intensity = value
                break

        # Extract current mood
        mood_indicators = {
            "happy": ["happy", "joyful", "excited", "cheerful"],
            "confident": ["confident", "proud", "accomplished"],
            "inspired": ["inspired", "motivated", "creative"],
            "focused": ["focused", "determined", "concentrated"],
            "tired": ["tired", "exhausted", "drained"],
            "nervous": ["nervous", "anxious", "worried"],
        }

        for mood, indicators in mood_indicators.items():
            if any(indicator in description for indicator in indicators):
                self.current_mood = mood
                break

    def update_mood(self, text: str):
        """Update mood based on text sentiment analysis."""
        mood_info = self._analyzer.analyze_mood(text)
        self.current_mood = mood_info["mood"]
        self.mood_intensity = mood_info["intensity"]

    def get_current_emotional_state(self) -> Dict[str, Any]:
        """Get the current emotional state."""
        return {
            "mood": self.current_mood,
            "intensity": self.mood_intensity,
            "stability": self.emotional_stability,
            "emoji_style": self.emoji_style,
        }

    def should_use_emoji(self) -> bool:
        """Determine if emoji should be used based on style and frequency."""
        return random.random() < self.emoji_style["frequency"]

    def get_emoji_count(self) -> int:
        """Get number of emojis to use based on style."""
        if not self.should_use_emoji():
            return 0
        return random.randint(1, self.emoji_style["max_per_post"])
