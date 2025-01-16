from fame.agent import Agent


def main():
    """Run physics professor tweet example."""
    print("\nInitializing physics professor agent...")
    agent = Agent(
        env_file=".env",
        facets_of_personality=(
            "A distinguished physics professor with a passion for making complex concepts "
            "accessible. Known for clear explanations and engaging teaching style. "
            "Combines deep technical knowledge with relatable analogies. "
            "Enthusiastic about sharing physics insights and discoveries."
        ),
        abilities_knowledge=(
            "Expert in quantum mechanics, particle physics, and theoretical physics. "
            "PhD in Physics with 15+ years teaching experience. "
            "Published researcher in quantum computing and quantum entanglement. "
            "Skilled at explaining complex physics concepts to general audiences."
        ),
        mood_emotions=(
            "Excited about sharing physics knowledge. "
            "Patient and encouraging when explaining difficult concepts. "
            "Maintains a balanced mix of professional expertise and approachable warmth."
        ),
        environment_execution=[],
    )

    try:
        print("\n=== Generating Physics Tweet ===")
        instruction = (
            "Share an insight about quantum physics, focusing on the wave-particle "
            "duality and the double-slit experiment. Make it engaging and "
            "accessible to a general audience while maintaining scientific accuracy."
        )
        print(f"\nInstruction: {instruction}")

        print("\nGenerating tweet content...")
        result = agent.post_tweet(instruction=instruction)

        print("\nTweet posting result:")
        print(f"Status: {result['status']}")
        print(f"Message: {result.get('message', 'No message provided')}")
        if result["status"] == "failed":
            print(f"\nFull result: {result}")

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback

        print(traceback.format_exc())


if __name__ == "__main__":
    main()
