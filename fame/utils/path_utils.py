import os
from typing import Optional


def resolve_profile_path(profile_path: str) -> Optional[str]:
    """
    Resolve profile image path relative to the execution directory.

    Args:
        profile_path: Path to profile image (relative or absolute)

    Returns:
        Absolute path to profile image or None if not found
    """
    # If it's an absolute path, verify it exists
    if os.path.isabs(profile_path):
        return profile_path if os.path.exists(profile_path) else None

    # Try relative to current working directory
    cwd_path = os.path.join(os.getcwd(), profile_path)
    if os.path.exists(cwd_path):
        return os.path.abspath(cwd_path)

    # Try relative to project root (one level up from cwd if in examples)
    if os.path.basename(os.getcwd()) == "examples":
        root_path = os.path.join(os.path.dirname(os.getcwd()), profile_path)
        if os.path.exists(root_path):
            return os.path.abspath(root_path)

    return None
