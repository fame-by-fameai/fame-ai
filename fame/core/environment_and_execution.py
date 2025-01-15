from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class EnvironmentAndExecution:
    platforms: List[str] = field(default_factory=list)
    available_actions: List[Dict[str, Any]] = field(default_factory=list)
    decision_logic: str = "contextual_analysis"
    execution_mechanisms: Dict[str, bool] = field(
        default_factory=lambda: {
            "api_integrations": True,
            "scheduling": True,
            "face_swap": True,
        }
    )
    schedule_config: Dict[str, Any] = field(
        default_factory=lambda: {
            "start_time": None,  # Default to now
            "end_time": None,  # Default to indefinite
            "post_frequency": "daily",
            "posts_per_day": 1,
        }
    )

    def to_dict(self):
        """Convert the object to a dictionary representation."""
        return {
            "platforms": self.platforms,
            "available_actions": self.available_actions,
            "decision_logic": self.decision_logic,
            "execution_mechanisms": self.execution_mechanisms,
            "schedule_config": self.schedule_config,
        }

    def add_platform(self, platform: str) -> None:
        """Add a new platform if it doesn't exist."""
        if platform not in self.platforms:
            self.platforms.append(platform)

    def add_action(self, action: Dict[str, Any]) -> None:
        """Add a new available action."""
        if action not in self.available_actions:
            self.available_actions.append(action)
