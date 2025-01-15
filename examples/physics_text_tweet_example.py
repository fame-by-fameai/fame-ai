from fame.agent import Agent
from pathlib import Path
from pprint import pprint


def setup_environment():
    """Ensure the environment is properly set up."""
    env_file = Path(".env")
    if not env_file.exists():
        print("Error: '.env' file not found. Please create it with your API keys.")
        return False
    return True


def main():
    if not setup_environment():
        return

    # Initialize the physics professor agent
    agent = Agent(
        env_file=".env",
        facets_of_personality=(
            "Dr. Alex Thompson is a witty and enthusiastic physics professor who loves "
            "making complex concepts accessible through humor. He has a talent for "
            "finding the fun in fundamental physics and enjoys creating clever analogies. "
            "While deeply knowledgeable about quantum mechanics and relativity, "
            "he never takes himself too seriously and loves dad jokes."
        ),
        abilities_knowledge=(
            "PhD in Theoretical Physics with 15 years of teaching experience. "
            "Expert in quantum mechanics, relativity, and particle physics. "
            "Skilled at breaking down complex concepts for general audiences. "
            "Known for creating memorable physics analogies and demonstrations. "
            "Combines academic expertise with pop culture references and humor."
        ),
        mood_emotions=(
            "Enthusiastic and playful while sharing knowledge. "
            "Gets excited about explaining physics concepts. "
            "Uses humor to make science more approachable. "
            "Enjoys creating 'aha moments' through clever explanations."
        ),
        environment_execution=[],
    )

    try:
        print("\n=== Generating Physics Tweet ===")

        # Generate the image prompt
        image_prompt = agent._generate_image_prompt(for_face_swap=False)

        # Generate tweet text based on the image prompt
        personality = agent.facets.get_personality_context()
        tweet_text = agent.openrouter_integration.generate_text(
            prompt=f"Write a tweet caption for an image of {image_prompt}, "
            f"in the style of {personality['traits'][0]}"
        )

        print("\nImage Generation Prompt:")
        print(image_prompt)

        print("\nTweet Text:")
        print(tweet_text)

        # Post the tweet using our generated prompts
        result = agent.post_image_tweet(
            prompt=image_prompt,  # Use our generated image prompt
            tweet_text=tweet_text,  # Use our generated tweet text
        )

        print("\nTweet posting result:")
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    main()
