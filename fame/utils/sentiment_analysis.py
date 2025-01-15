from typing import Dict, Any
from fame.integrations.openrouter_integration import OpenRouterIntegration


class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analyzer."""
        self.openrouter = None  # Will be set when needed

    def set_openrouter(self, openrouter: OpenRouterIntegration):
        """Set OpenRouter integration instance."""
        self.openrouter = openrouter

    def analyze_mood(self, text: str) -> Dict[str, Any]:
        """Analyze text sentiment using OpenRouter LLM."""
        if not self.openrouter:
            return {"mood": "neutral", "intensity": 0.5}

        prompt = f"""
        Analyze the emotional tone and mood of this text:
        "{text}"
        
        Return only a JSON object with two fields:
        - mood: one of [enthusiastic, happy, neutral, concerned, frustrated]
        - intensity: float between 0.0 and 1.0 indicating strength of the mood
        
        Example: {{"mood": "enthusiastic", "intensity": 0.8}}
        """

        response = self.openrouter.generate_text(prompt)

        try:
            # Parse the response as JSON
            import json

            mood_data = json.loads(response)
            return {
                "mood": mood_data.get("mood", "neutral"),
                "intensity": float(mood_data.get("intensity", 0.5)),
            }
        except:
            # Fallback to neutral if parsing fails
            return {"mood": "neutral", "intensity": 0.5}
