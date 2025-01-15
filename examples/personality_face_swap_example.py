from fame.agent import Agent
import os
from pathlib import Path


def setup_environment():
    """Ensure the environment is properly set up."""
    # Check for profile image
    profile_path = Path("profiles/bonnie.jpg")
    if not profile_path.exists():
        print(f"Error: Profile image not found at {profile_path}")
        return False

    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("Error: '.env' file not found. Please create it with your API keys.")
        return False

    return True


def main():
    if not setup_environment():
        return

    # Initialize agent with a specific personality
    agent = Agent(
        env_file=".env",
        facets_of_personality=(
            "Bonnie is a passionate 17-year-old ballet dancer who loves performing "
            "and sharing her dance journey. She's dedicated to her craft, "
            "maintains a positive attitude, and inspires others through social media. "
            "She has a graceful presence and enjoys both classical and contemporary dance."
        ),
        abilities_knowledge=(
            "Professional level ballet training with 10 years of experience. "
            "Skilled in contemporary dance, choreography, and performance. "
            "Knowledgeable about dance history and technique. "
            "Experienced in social media content creation and dance photography."
        ),
        mood_emotions=(
            "Excited and inspired after a successful dance rehearsal. "
            "Feeling confident and eager to share her progress with followers. "
            "Full of creative energy and joy from dancing."
        ),
        environment_execution=[],  # No scheduling needed for this example
        profile_image_path="profiles/bonnie.jpg",
    )

    try:
        print("\nGenerating scene based on personality...")
        # Generate the prompt first
        prompt = agent._generate_base_image_prompt()
        print("\nGenerated prompt:", prompt)
        print("\nStarting face swap with this prompt...")

        # Use the generated prompt for face swap
        result = agent.post_face_tweet(base_image_prompt=prompt)
        print("\nFace swap result:", result)

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    main()
