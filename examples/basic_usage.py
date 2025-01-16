from fame.agent import Agent


def main():
    """Run basic usage example with both text and face-swapped image tweets."""
    print("\nInitializing basic agent...")

    # Initialize the agent with minimal configuration
    agent = Agent(
        env_file=".env",
        facets_of_personality=(
            "Bonnie is a friendly and cheerful girl who likes dancing and studying "
            "in high school"
        ),
        abilities_knowledge=(
            "She has strong dancing skills and high school level knowledge in the "
            "United States"
        ),
        mood_emotions=("generally happy but sometimes gets stressed about exams"),
        environment_execution=[],  # Empty list for no scheduling
        profile_image_path="profiles/bonnie.jpg",
    )

    try:
        # Example 1: Simple text tweet
        print("\n=== Posting Simple Tweet ===")
        text_result = agent.post_tweet(
            instruction="Share your excitement about an upcoming dance performance"
        )

        print("\nText tweet result:")
        print(f"Status: {text_result['status']}")
        print(f"Message: {text_result.get('message', 'No message provided')}")
        if text_result["status"] == "failed":
            print(f"\nFull result: {text_result}")

        # Example 2: Face-swapped image tweet
        print("\n=== Posting Face-Swapped Image Tweet ===")
        image_result = agent.post_image_tweet(
            prompt="",
            tweet_text="",  # Will be generated from the image
            use_face_swap=True,  # Enable face swapping
        )

        print("\nImage tweet result:")
        print(f"Status: {image_result['status']}")
        print(f"Message: {image_result.get('message', 'No message provided')}")
        if image_result["status"] == "failed":
            print(f"\nFull result: {image_result}")

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback

        print(traceback.format_exc())


if __name__ == "__main__":
    main()
