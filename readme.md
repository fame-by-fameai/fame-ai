# FAME Framework 🚀

FAME Framework (Full AI Meta Engine) is an AI agent framework designed to simulate human-like interactions and content creation on social media platforms.

## Installation

You can install FAME from PyPI:

```bash
pip install fame-agent
```

For development installation:

```bash
pip install fame-agent[dev]
```

## Quick Start

```python
from fame.agent import Agent

# Initialize agent
agent = Agent(
    env_file=".env",
    facets_of_personality="A tech startup founder focused on innovation...",
    abilities_knowledge="Expert in: AI/ML architecture, sustainable computing...",
    mood_emotions="Enthusiastic about sharing startup knowledge...",
    environment_execution=[]
)

# Post a tweet
result = agent.post_image_tweet()
```

The project consists of several modules that handle different aspects of the agent's behavior:

- **Facets of Personality**: Defined by traits, interests, communication style, etc. 🌈
- **Abilities and Knowledge**: Expertise in specific fields, skills, and experience level. 🎓
- **Mood and Emotions**: Current emotional state and intensity. 😃😢
- **Environment and Execution**: Scheduling of posts and integration with Twitter. 📅🐦

## Table of Contents 📚

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
  - [fame/](#fame)
  - [Configuration Files](#configuration-files)
  - [Integrations](#integrations)
  - [Utilities](#utilities)
  - [Core Components](#core-components)
- [Contributing](#contributing)
- [License](#license)

## Usage🛠️

Once installed, you can run the agent to automate posting activities on Twitter:

1. Initialize an `Agent` instance:

   ```python
   from fame.agent import Agent

   # Load your configurations and profiles here
   agent = Agent(
       facets_of_personality="path/to/facets.json",
       abilities_knowledge="path/to/abilities.json",
       mood_emotions="path/to/mood.json"
       # Additional parameters...
   )

   # To post a tweet
   agent.post_tweet("Hello, world!")
   ```

2. Schedule automated posts using background schedulers.⏰

## Project Structure🏗️

### `fame/`

The main package directory containing all modules and classes required to run the Fame agent. Key files include:

- `__init__.py`: Makes the directory a Python package.
- `agent.py`: Main class for managing agent behaviors, including posting tweets and generating content.

### Configuration Files 📄

Configuration files define default parameters and model configurations. These can be customized as needed:

- `openrouter_models.py`: Default OpenRouter model configurations.
- `replicate_models.py`: Default Replicate model configurations.

### Integrations🔗

Modules handling integrations with various APIs and platforms for seamless interaction:

- `openrouter_integration.py`: Integration with OpenRouter AI models for text generation and chat functionalities.
- `replicate_integration.py`: Integration with Replicate for image generation and face swap capabilities.
- `twitter_integration.py`: Handles interactions with the Twitter API.

### Core Components 🧩

Core modules that define various facets of agent behavior:

- `abilities_and_knowledge.py`: Manages agent's skills, knowledge areas, and expertise.
- `facets_of_personality.py`: Encapsulates personality traits and communication styles.
- `mood_and_emotions.py`: Handles mood tracking and emotional states.

### Utilities 🛠️

Utility modules providing helper functions and tools:

- `path_utils.py`: Resolves file paths for profile images.
- `sentiment_analysis.py`: Performs sentiment analysis using OpenRouter LLM integration.
- `tweet_validator.py`: Validates tweet content against Twitter's requirements.

## Conclusion 🎉

The Fame project provides a robust framework for creating an AI-driven agent capable of automated interactions on social media platforms. With configurable integrations and flexible core components, it allows for extensive customization to meet various needs in content generation and social media automation.
