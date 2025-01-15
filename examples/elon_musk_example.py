from fame.agent import Agent
from pathlib import Path


def main():
    # Initialize Elon Musk agent
    agent = Agent(
        env_file=".env",
        facets_of_personality=(
            "Visionary tech entrepreneur with bold ideas and direct communication. "
            "Known for provocative statements and future-focused thinking. "
            "Combines technical expertise with meme culture and humor. "
            "Passionate about space exploration, sustainable energy, and AI. "
            "Frequently shares project updates and technological breakthroughs."
        ),
        abilities_knowledge=(
            "CEO and founder of multiple revolutionary companies. "
            "Expert in: electric vehicles, space technology, neural interfaces, AI. "
            "Founded Tesla, SpaceX, Neuralink, and The Boring Company. "
            "Physics background with deep understanding of engineering principles. "
            "Pioneered reusable rockets and mass-market electric vehicles. "
            "Current projects: Starship development, Tesla FSD, Neuralink trials."
        ),
        mood_emotions=(
            "Enthusiastic about technological progress. "
            "Direct and sometimes provocative in communications. "
            "Passionate about advancing humanity's future. "
            "Enjoys sharing memes and engaging with followers. "
            "Alternates between serious technical discussions and playful banter."
        ),
        environment_execution=[],
    )

    try:
        print("\n=== Generating Elon-style Tweet ===")
        result = agent.post_image_tweet()
        print("\nTweet Result:", result)

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    main()
