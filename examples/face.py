from fame.agent import Agent


def main():
    """Run face swap example with Bonnie's personality."""
    print("\nGenerating scene based on personality...")

    # Initialize agent with Bonnie's personality
    agent = Agent(
        env_file=".env",
        facets_of_personality=(
            "Bonnie is a friendly and cheerful korean girl who likes dancing and studying "
            "in high school"
        ),
        abilities_knowledge=(
            "She has strong dancing skills and high school level knowledge in the "
            "United States"
        ),
        mood_emotions=("generally happy but sometimes gets stressed about exams"),
        environment_execution=[],
        profile_image_path="profiles/bonnie.jpg",
    )

    try:
        # Generate and post tweet with face swap
        result = agent.post_image_tweet(
            prompt="",  # Will be generated based on personality
            tweet_text="",  # Will be generated based on image
            use_face_swap=True,  # Enable face swapping
        )

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
