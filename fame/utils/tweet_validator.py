import re
from typing import Tuple


class TweetValidator:
    """Validates and cleans tweet content."""

    def __init__(self):
        self.max_length = 280
        self.url_length = 23  # Twitter treats all URLs as 23 characters

    def clean_tweet_text(self, text: str) -> str:
        """Clean and format tweet text."""
        # Remove extra whitespace
        text = " ".join(text.split())

        # Remove quotes if they wrap the entire text
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1].strip()

        # Remove face swap instructions in parentheses
        text = re.sub(r"\s*\*.*?\*\s*$", "", text)

        # Normalize hashtags (ensure # is directly followed by text)
        text = re.sub(r"#\s+", "#", text)

        return text.strip()

    def validate_tweet(self, text: str) -> Tuple[bool, str]:
        """
        Validate tweet content.

        Returns:
            Tuple of (is_valid, reason)
        """
        if not text:
            return False, "Tweet is empty"

        # Calculate length considering URL shortening
        length = len(text)
        urls = re.findall(r"https?://\S+", text)
        for url in urls:
            length = length - len(url) + self.url_length

        if length > self.max_length:
            return False, f"Tweet exceeds {self.max_length} characters"

        return True, "Valid tweet"
