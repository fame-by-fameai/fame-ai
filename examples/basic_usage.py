from fame.agent import Agent


def main():
    # Initialize the agent with minimal configuration
    agent = Agent(
        env_file=".env",
        facets_of_personality="Bonnie is a friendly and cheerful girl who likes dancing and studying in high school",
        abilities_knowledge="She has strong dancing skills and high school level knowledge in the United States",
        mood_emotions="generally happy but sometimes gets stressed about exams",
        environment_execution=[],  # Empty list for no scheduling
        profile_image_path="profiles/bonnie.jpg",
    )

    # Direct posting without scheduling
    result = agent.post_tweet(
        instruction="Share your excitement about an upcoming dance performance"
    )
    print("Tweet result:", result)


if __name__ == "__main__":
    main()
