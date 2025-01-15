import re
from typing import Dict, Tuple


class TweetValidator:
    MAX_TWEET_LENGTH = 280
    MIN_TWEET_LENGTH = 1
    URL_LENGTH = 23  # Twitter treats all URLs as 23 characters

    @staticmethod
    def validate_tweet(content: str) -> tuple[bool, dict]:
        """
        Validate a tweet content.
        Returns (is_valid, details)
        """
        # Remove any character count text that might be included
        content = TweetValidator._clean_tweet_text(content)

        issues = []
        suggestions = []

        # Check length
        char_count = len(content)
        if char_count > 280:
            issues.append(f"Tweet is too long ({char_count} characters)")
            suggestions.append("Shorten the tweet to 280 characters or less")

        # Other validation checks...

        return len(issues) == 0, {"issues": issues, "suggestions": suggestions}

    @staticmethod
    def _clean_tweet_text(text: str) -> str:
        """Remove metadata like character counts from tweet text."""
        # Remove character count patterns
        patterns = [
            r"\(Character count: \d+\)",
            r"\[Characters: \d+\]",
            r"Character count: \d+",
            r"\d+ characters",
        ]

        cleaned_text = text
        for pattern in patterns:
            cleaned_text = re.sub(pattern, "", cleaned_text, flags=re.IGNORECASE)

        # Remove trailing whitespace
        cleaned_text = cleaned_text.strip()

        return cleaned_text
