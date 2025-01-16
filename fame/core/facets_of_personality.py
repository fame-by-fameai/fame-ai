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
        self.demographics = self._extract_demographics(description)

    def _extract_demographics(self, description: str) -> Dict[str, str]:
        """Extract demographic information from personality description."""
        try:
            # Build prompt for demographic extraction
            prompt = (
                f"Extract demographic information from this description:\n"
                f"{description}\n\n"
                f"Return ONLY an array with exactly 3 strings in this order: [age, gender, ethnicity]\n"
                f'Example: ["teenager", "female", "korean"]\n\n'
                f"- Age should be general (child, teenager, young adult, adult, elderly)\n"
                f"- Gender should be male or female\n"
                f"- Ethnicity should be specific (korean, chinese, caucasian, etc)\n"
                f"Return only the array, no other text or formatting."
            )

            # Get demographics from LLM
            response = self.llm.generate_text(prompt=prompt)
            if not response:
                return {}

            try:
                # Clean and parse response
                cleaned = response.strip()
                if not cleaned.startswith("["):
                    # Try to find array in response
                    import re

                    match = re.search(r"\[(.*?)\]", cleaned, re.DOTALL)
                    if match:
                        cleaned = match.group(0)
                    else:
                        return {}

                # Parse array
                import json

                demographics = json.loads(cleaned)

                if not isinstance(demographics, list) or len(demographics) != 3:
                    return {}

                # Convert to dictionary
                return {
                    "age": demographics[0].lower(),
                    "gender": demographics[1].lower(),
                    "ethnicity": demographics[2].lower(),
                }

            except json.JSONDecodeError:
                print(f"Error parsing demographics response: {response}")
                return {}

        except Exception as e:
            print(f"Error extracting demographics: {str(e)}")
            return {}

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
