from dataclasses import dataclass, field
from typing import List, Dict, Any
import re


@dataclass
class FacetsOfPersonality:
    core_traits: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    communication_style: str = "professional"
    current_style: str = "informative"

    def __init__(self, description: str):
        """Initialize personality from description."""
        self.raw_description = description
        self._parse_description()

    def _parse_description(self):
        """Parse the description to extract personality traits."""
        description = self.raw_description.lower()

        # Professional trait keywords
        trait_keywords = {
            # Leadership traits
            "visionary": ["visionary", "pioneering", "innovative", "forward-thinking"],
            "leader": ["leader", "executive", "founder", "director", "manager"],
            "strategic": ["strategic", "analytical", "methodical", "systematic"],
            # Communication traits
            "articulate": ["articulate", "eloquent", "expressive", "communicative"],
            "engaging": ["engaging", "charismatic", "captivating", "inspiring"],
            "direct": ["direct", "straightforward", "clear", "concise"],
            # Teaching traits
            "educator": ["educator", "teacher", "instructor", "mentor", "coach"],
            "explanatory": [
                "explanatory",
                "informative",
                "educational",
                "enlightening",
            ],
            "patient": ["patient", "understanding", "supportive", "helpful"],
            # Technical traits
            "technical": ["technical", "analytical", "precise", "detailed"],
            "expert": ["expert", "specialist", "authority", "professional"],
            "innovative": ["innovative", "creative", "inventive", "original"],
            # Personal traits
            "enthusiastic": ["enthusiastic", "passionate", "energetic", "dynamic"],
            "witty": ["witty", "humorous", "clever", "funny"],
            "approachable": ["approachable", "friendly", "accessible", "relatable"],
        }

        # Professional interests and domains
        interest_keywords = {
            # Technology
            "technology": ["tech", "technology", "digital", "software", "computing"],
            "ai_ml": [
                "ai",
                "machine learning",
                "artificial intelligence",
                "data science",
            ],
            "robotics": ["robotics", "automation", "mechatronics", "control systems"],
            # Business
            "business": ["business", "entrepreneurship", "management", "strategy"],
            "startup": ["startup", "venture", "entrepreneurial", "scaling"],
            "innovation": ["innovation", "development", "r&d", "advancement"],
            # Science
            "physics": ["physics", "quantum", "theoretical", "applied science"],
            "research": ["research", "investigation", "study", "analysis"],
            "engineering": ["engineering", "systems", "design", "development"],
            # Education
            "teaching": ["teaching", "education", "instruction", "training"],
            "mentoring": ["mentoring", "coaching", "guidance", "development"],
            "knowledge_sharing": ["knowledge sharing", "learning", "education"],
            # Creative
            "design": ["design", "creative", "artistic", "visual"],
            "content": ["content", "media", "digital media", "creation"],
            "communication": ["communication", "writing", "speaking", "presenting"],
            # Sustainability
            "sustainability": ["sustainability", "green tech", "eco-friendly"],
            "environment": ["environmental", "climate", "conservation"],
            "renewable": ["renewable", "clean energy", "sustainable"],
        }

        # Extract core professional traits
        self.core_traits = []
        professional_indicators = [
            "founder",
            "educator",
            "researcher",
            "developer",
            "expert",
            "professional",
            "specialist",
            "leader",
        ]

        for indicator in professional_indicators:
            if indicator in description:
                self.core_traits.append(indicator)

        # Extract professional interests
        self.interests = []
        for field, keywords in interest_keywords.items():
            if any(keyword in description for keyword in keywords):
                self.interests.append(field)

        # Determine communication style
        for style, indicators in communication_styles.items():
            if any(indicator in description for indicator in indicators):
                self.communication_style = style
                break

        # Set current style based on context
        style_indicators = {
            "informative": ["explain", "teach", "share", "inform"],
            "analytical": ["analyze", "examine", "investigate"],
            "strategic": ["plan", "develop", "implement"],
            "innovative": ["create", "design", "innovate"],
        }

        for style, indicators in style_indicators.items():
            if any(indicator in description for indicator in indicators):
                self.current_style = style
                break

    def get_personality_context(self) -> Dict[str, Any]:
        """Get comprehensive personality context."""
        return {
            "traits": self.core_traits,
            "interests": self.interests,
            "communication_style": self.communication_style,
            "current_style": self.current_style,
        }
