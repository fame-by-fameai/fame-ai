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

    # Initialize the startup founder agent
    agent = Agent(
        env_file=".env",
        facets_of_personality=(
            "A tech startup founder focused on innovation and sustainable solutions. "
            "Combines technical expertise with business vision. "
            "Known for clear communication and explaining complex concepts. "
            "Professional approach with emphasis on knowledge sharing. "
            "Dedicated to continuous learning and industry advancement."
        ),
        abilities_knowledge=(
            "MS in Computer Science with focus on Machine Learning. "
            "Expert in: AI/ML architecture, sustainable computing, green tech solutions. "
            "Specialized knowledge: neural networks, energy-efficient algorithms, "
            "carbon footprint optimization, startup scaling methodologies. "
            "Published research on eco-friendly AI systems and sustainable cloud computing. "
            "Developed patented green computing algorithms and sustainability metrics."
        ),
        mood_emotions=(
            "Enthusiastic about sharing startup knowledge. "
            "Passionate about educating others on sustainable tech. "
            "Analytical yet approachable when explaining complex concepts. "
            "Excited to showcase practical applications and real-world impact."
        ),
        environment_execution=[],
    )

    try:
        print("\n=== Generating Sharing Content ===")

        # Let the agent generate and post content based on its expertise
        result = agent.post_image_tweet()

        print("\nPost Result:")
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    main()
