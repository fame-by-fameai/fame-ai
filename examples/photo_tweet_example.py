from fame.agent import Agent
import os
from pathlib import Path


def setup_environment():
    """Ensure the environment is properly set up."""
    # Try different possible profile image locations
    possible_paths = [
        Path("../profiles/bonnie.jpg"),  # Relative to examples dir
        Path("profiles/bonnie.jpg"),  # Relative to project root
        Path(os.getcwd()) / "profiles/bonnie.jpg",  # Absolute from current dir
    ]

    profile_image = None
    for path in possible_paths:
        if path.exists():
            profile_image = path
            break

    if not profile_image:
        raise FileNotFoundError(
            "Profile image 'bonnie.jpg' not found. Please ensure it exists in either:\n"
            f"- {possible_paths[0]}\n"
            f"- {possible_paths[1]}\n"
            f"- {possible_paths[2]}"
        )

    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        raise FileNotFoundError(
            "'.env' file not found. Please create it with your API keys and credentials."
        )

    return profile_image


def main():
    # Ensure environment is set up and get correct profile path
    profile_image_path = setup_environment()

    # Initialize the agent with detailed configuration
    agent = Agent(
        env_file=".env",
        facets_of_personality=(
            "Bonnie is a friendly and cheerful 17-year-old high school student. "
            "She's passionate about dance, especially ballet and contemporary. "
            "She's diligent in her studies and maintains a positive attitude. "
            "She loves sharing her dance journey and student life on social media."
        ),
        abilities_knowledge=(
            "Expert in ballet and contemporary dance with 10 years of training. "
            "Strong academic performance in high school, especially in literature and arts. "
            "Skilled at social media content creation and engaging with followers. "
            "Basic photography and image editing skills."
        ),
        mood_emotions=(
            "Generally cheerful and optimistic, with occasional stress about dance "
            "performances and exams. Shows enthusiasm for learning and performing. "
            "Empathetic towards fellow students and dancers."
        ),
        environment_execution=[],  # Empty list for no scheduling
        profile_image_path=str(profile_image_path),  # Use the found path
    )

    try:
        # Post a face-swapped image tweet
        print("\nPosting face-swapped image tweet...")
        base_image_prompt = (
            "A graceful ballet dancer in a beautiful pose, wearing a light pink "
            "leotard and tutu, practicing in front of studio mirrors. The lighting "
            "is soft and warm, creating an inspiring atmosphere for dance."
        )
        result = agent.post_face_tweet(base_image_prompt=base_image_prompt)
        print("Result:", result)

        if result["status"] == "failed":
            print("Failed to post face-swapped image tweet:", result["message"])

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
