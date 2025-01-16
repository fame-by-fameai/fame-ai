from fame.agent import Agent


def main():
    """Run photo tweet example."""
    print("\nPosting face-swapped image tweet...")

    # Initialize agent with photographer personality
    agent = Agent(
        env_file=".env",
        facets_of_personality=(
            "A passionate photographer with an eye for capturing unique moments. "
            "Known for creative compositions and artistic vision. "
            "Loves sharing photography tips and inspiring others."
        ),
        abilities_knowledge=(
            "Expert in digital photography and photo editing. "
            "Skilled at composition, lighting, and visual storytelling. "
            "Experienced in both studio and outdoor photography."
        ),
        mood_emotions=(
            "Excited to share creative work. "
            "Inspired by beautiful scenes and moments. "
            "Enthusiastic about helping others improve their photography."
        ),
        environment_execution=[],
        profile_image_path="profiles/bonnie.jpg",
    )

    try:
        # Generate and post tweet with face swap
        result = agent.post_image_tweet(
            prompt=(
                "A professional photographer in a sunlit studio, surrounded by "
                "high-end camera equipment and stunning photo displays. The scene "
                "captures the perfect blend of technical expertise and artistic vision."
            ),
            tweet_text="",  # Will be generated from the image
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
