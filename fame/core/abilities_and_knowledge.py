from dataclasses import dataclass, field
from typing import List, Dict, Any
import re


@dataclass
class AbilitiesAndKnowledge:
    expertise: List[str] = field(default_factory=list)
    primary_field: str = "general"
    specialties: List[str] = field(default_factory=list)
    experience_level: str = "intermediate"
    role: str = "professional"
    skills: List[Dict[str, float]] = field(default_factory=list)
    raw_description: str = ""

    def __post_init__(self):
        """Initialize after dataclass fields are set."""
        self._parse_description()

    def __init__(self, description: str):
        """Initialize abilities and knowledge from description."""
        super().__init__()
        self.raw_description = description
        self.expertise = []
        self.specialties = []
        self.skills = []
        self._parse_description()

    def _parse_description(self):
        """Parse the description to extract abilities and knowledge."""
        description = self.raw_description.lower()

        # Clear existing lists before parsing
        self.expertise = []
        self.specialties = []
        self.skills = []

        # Extract expertise areas
        expertise_patterns = [
            r"expert in ([^\.]+)",
            r"specialized in ([^\.]+)",
            r"expertise in ([^\.]+)",
        ]

        for pattern in expertise_patterns:
            matches = re.finditer(pattern, description)
            for match in matches:
                self.expertise.extend(
                    [exp.strip() for exp in match.group(1).split(",")]
                )

        # Extract primary field
        field_patterns = [
            r"phd in ([^\.]+)",
            r"ms in ([^\.]+)",
            r"master in ([^\.]+)",
            r"specializing in ([^\.]+)",
        ]

        for pattern in field_patterns:
            match = re.search(pattern, description, re.I)
            if match:
                self.primary_field = match.group(1).strip()
                break

        # Extract specialties with expanded categories
        specialty_indicators = {
            "ai_ml": [
                "machine learning",
                "artificial intelligence",
                "neural networks",
                "ai/ml",
            ],
            "sustainability": [
                "sustainable",
                "green tech",
                "eco-friendly",
                "carbon footprint",
            ],
            "business": ["startup", "entrepreneurship", "business", "scaling"],
            "technology": ["computing", "algorithms", "tech solutions", "architecture"],
            "innovation": ["innovation", "research", "development", "patents"],
            "physics": ["quantum mechanics", "relativity", "particle physics"],
            "teaching": ["education", "teaching", "instruction"],
            "research": ["research", "investigation", "study"],
        }

        for specialty, indicators in specialty_indicators.items():
            if any(indicator in description for indicator in indicators):
                self.specialties.append(specialty)

        # Determine experience level
        experience_indicators = {
            "expert": ["expert", "advanced", "seasoned", "veteran"],
            "intermediate": ["experienced", "proficient", "skilled"],
            "beginner": ["junior", "beginning", "learning"],
        }

        for level, indicators in experience_indicators.items():
            if any(indicator in description for indicator in indicators):
                self.experience_level = level
                break

        # Extract role
        role_patterns = [
            r"(founder|ceo|owner|executive|leader)",
            r"(professor|teacher|instructor|researcher|scientist)",
            r"(engineer|developer|architect)",
            r"(phd|doctorate|master)",
        ]

        for pattern in role_patterns:
            match = re.search(pattern, description, re.I)
            if match:
                self.role = match.group(1).lower()
                break

    def get_knowledge_context(self) -> Dict[str, Any]:
        """Get comprehensive knowledge and abilities context."""
        return {
            "expertise": self.expertise,
            "primary_field": self.primary_field,
            "specialties": self.specialties,
            "experience_level": self.experience_level,
            "role": self.role,
            "skills": self.skills,
        }
