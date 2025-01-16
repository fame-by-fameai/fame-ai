from typing import Dict
from fame.integrations.openrouter_integration import OpenRouterIntegration


class FacetsOfPersonality:
    """Core personality traits and characteristics."""

    def __init__(self, description: str, llm: OpenRouterIntegration):
        """
        Initialize personality facets.

        Args:
            description: Personality description
            llm: OpenRouter integration instance
        """
        self.description = description
        self.llm = llm
        self.demographics = self._extract_demographics()

    def _extract_demographics(self) -> Dict[str, str]:
        """Extract demographic information from description using LLM."""
        prompt = (
            f"Extract demographic information from this personality description:\n"
            f"{self.description}\n\n"
            f"Return only a JSON object with these fields:\n"
            f'{{"gender": "...", "age": "...", "ethnicity": "..."}}\n\n'
            f'Example: {{"gender": "female", "age": "teenager", "ethnicity": "white"}}\n'
            f"Use 'unknown' if a field cannot be determined."
        )

        try:
            response = self.llm.generate_text(prompt=prompt)

            # Parse JSON response
            import json

            demographics = json.loads(response)
            return demographics

        except Exception as e:
            print(f"Error extracting demographics: {str(e)}")
            return {"gender": "unknown", "age": "unknown", "ethnicity": "unknown"}

    def get_personality_context(self) -> str:
        """Get full personality context including demographics."""
        demo = self.demographics
        demographic_str = (
            f"{demo.get('age', 'unknown')} "
            f"{demo.get('gender', 'unknown')} "
            f"{demo.get('ethnicity', 'unknown')}"
        ).strip()

        return (
            f"Demographics: {demographic_str if demographic_str else 'Not specified'}\n"
            f"Personality: {self.description}"
        )
