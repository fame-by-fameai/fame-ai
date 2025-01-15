import re
from typing import Dict, List, Any, Tuple


def extract_traits_from_text(text: str) -> Tuple[List[str], List[str]]:
    """Extract personality traits and interests from text description."""
    # Basic trait extraction (this could be enhanced with NLP)
    traits = []
    interests = []

    # Look for common descriptive words
    words = text.lower().split()

    # Simple trait keywords
    trait_keywords = ["friendly", "outgoing", "shy", "creative", "analytical"]
    interest_keywords = ["likes", "enjoys", "interested", "passionate"]

    for word in words:
        if word in trait_keywords:
            traits.append(word)

    # Extract interests (words after "likes", "enjoys", etc.)
    text_lower = text.lower()
    for keyword in interest_keywords:
        if keyword in text_lower:
            # Find the word after the keyword
            pattern = f"{keyword}\s+(\w+)"
            matches = re.findall(pattern, text_lower)
            interests.extend(matches)

    return traits, interests


def parse_facets_of_personality(text: str) -> Dict[str, Any]:
    """Parse personality description into structured data."""
    traits, interests = extract_traits_from_text(text)

    return {
        "core_traits": traits,
        "interests": interests,
        "communication_style": "friendly",  # Default value
        "values": [],
        "temperament": "balanced",  # Default value
    }


def parse_abilities_knowledge(text: str) -> Dict[str, Any]:
    """Parse abilities and knowledge description into structured data."""
    # Extract skills (words after "skills in" or similar patterns)
    skills = []
    skill_pattern = r"skills?\s+in\s+(\w+)"
    matches = re.findall(skill_pattern, text.lower())
    skills.extend(matches)

    # Extract knowledge areas
    knowledge = {}
    knowledge_pattern = r"knowledge\s+in\s+(\w+)"
    matches = re.findall(knowledge_pattern, text.lower())
    for area in matches:
        knowledge[area] = "basic"  # Default level

    return {"skills": skills, "domain_knowledge": knowledge}


def parse_mood_emotions(text: str) -> Dict[str, Any]:
    """Parse mood and emotions description into structured data."""
    # Basic mood keywords
    mood_keywords = {
        "happy": 0.8,
        "sad": -0.5,
        "angry": -0.8,
        "excited": 1.0,
        "neutral": 0.0,
    }

    current_mood = "neutral"
    mood_intensity = 0.0

    text_lower = text.lower()
    for mood, intensity in mood_keywords.items():
        if mood in text_lower:
            current_mood = mood
            mood_intensity = intensity
            break

    return {
        "current_mood": current_mood,
        "mood_intensity": mood_intensity,
        "triggers": [],
        "mood_history": [],
    }


def parse_environment_execution(env_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Parse environment and execution configuration."""
    platforms = []
    actions = []

    for item in env_list:
        platform = item.get("platform", "")
        if platform:
            platforms.append(platform)

        functions = item.get("function", [])
        if isinstance(functions, str):
            functions = [functions]

        for func in functions:
            actions.append(
                {
                    "name": func,
                    "platform": platform,
                    "description": f"Perform {func} on {platform}",
                    "parameters": [],
                }
            )

    return {
        "platforms": platforms,
        "available_actions": actions,
        "decision_logic": "contextual_analysis",
        "execution_mechanisms": {"api_integrations": True, "scheduling": False},
    }
