# FAME Framework 🚀

FAME is an advanced AI agent framework designed to simulate human-like interactions and create engaging content specifically for social media platforms, with a focus on Twitter. It generates dynamic content — from images and text to videos — that reflects the agent's personality, knowledge, and current mood. 🎨📝

Key Modules of the FAME Framework:
**Facets of Personality**
•⁠ ⁠Defined by traits, interests, and communication style. 🎨
**Abilities and Knowledge**
•⁠ ⁠Expertise in specific fields, skills, and experience level. 🎓
**Mood and Emotions**
•⁠ ⁠Reflects the agent's current emotional state and intensity. 😊😢
**Environment and Execution**
•⁠ ⁠Handles scheduling of posts and seamless integration with Twitter. 📅🐦

## Installation

Install the package using pip:

```bash
pip install fame-ai
```

## Quick Start

1. Create a `.env` file with your API keys:

```env
# Twitter/X API Credentials
X_CONSUMER_KEY=your_consumer_key_here
X_CONSUMER_SECRET=your_consumer_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_TOKEN_SECRET=your_access_token_secret_here

# AI Service API Keys
REPLICATE_API_KEY=your_replicate_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
```

2. Create a profile image for your agent in a `profiles` directory:

```bash
mkdir profiles
# Add your agent's profile image as profiles/your_image.jpg
```

3. Basic usage example:

```python
from fame.agent import Agent

# Initialize agent with personality
agent = Agent(
    env_file=".env",
    facets_of_personality=(
        "Bonnie is a friendly and cheerful Korean girl who likes dancing "
        "and studying in high school"
    ),
    abilities_knowledge=(
        "She has strong dancing skills and high school level knowledge "
        "in the United States"
    ),
    mood_emotions="generally happy but sometimes gets stressed about exams",
    environment_execution=[],  # Empty list for no scheduling
    profile_image_path="profiles/bonnie.jpg",
)

# Post a simple text tweet
text_result = agent.post_tweet(
    instruction="Share your excitement about an upcoming dance performance"
)

# Post a tweet with face-swapped image
image_result = agent.post_image_tweet(
    prompt="",  # Will be generated based on personality
    tweet_text="",  # Will be generated based on image
    use_face_swap=True,  # Enable face swapping
)
```

## Features

- 🤖 Personality-driven content generation
- 🎭 Face swapping with profile images
- 📝 Natural text generation
- 🖼️ AI image generation
- 📅 Scheduled posting (optional)
- 🔄 Twitter/X API integration

## Requirements

- Python 3.8+
- Twitter/X Developer Account with API access
- Replicate API key
- OpenRouter API key

## Documentation

For more detailed examples and API documentation, visit our [documentation site](https://docs.getfame.ai).

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
