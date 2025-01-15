from fame.agent import Agent
from pathlib import Path
import json
from pprint import pprint


def setup_environment():
    """Ensure the environment is properly set up."""
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("Error: '.env' file not found. Please create it with your API keys.")
        return False
    return True


def main():
    if not setup_environment():
        return

    # Initialize agent as a physics professor
    agent = Agent(
        env_file=".env",
        facets_of_personality=(
            "Dr. Alex Thompson is a witty and enthusiastic physics professor who loves making complex concepts accessible through humor. He has a talent for finding the fun in fundamental physics and enjoys creating clever analogies. While deeply knowledgeable about quantum mechanics and relativity, he never takes himself too seriously and loves dad jokes."
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
        environment_execution=[],  # No scheduling needed for this example
    )

    try:
        print("\n=== Testing Physics Professor's Tweet Drafts ===")
        # Generate a week of daily posts
        weekly_schedule = agent.draft_scheduled_posts(
            posts_per_day=1, interval="day", duration=7
        )

        # Save full schedule
        save_schedule(weekly_schedule, "physics_professor_schedule.json")

        # Print some example tweets
        print("\nExample Tweet Drafts:")
        for post in weekly_schedule:
            if post["post_type"] == "text":
                print(f"\nDay {post['day']} - {post['topic']}:")
                print(post["content"]["text"])

        # Test individual content generation
        print("\n=== Testing Individual Content Types ===")
        personality = agent.facets.get_personality_context()

        print("\nPhysics Concept Tweet:")
        text_content = agent._generate_draft_content(
            post_type="text",
            topic="Quantum superposition",
            personality=personality,
        )
        pprint(text_content)

        print("\nPhysics Analogy Tweet:")
        text_content = agent._generate_draft_content(
            post_type="text",
            topic="Special relativity explained with coffee",
            personality=personality,
        )
        pprint(text_content)

        # When generating a physics-focused image
        physics_prompt = (
            "A complex quantum mechanics equation being solved on a transparent glass board, "
            "with colorful diagrams showing particle interactions and wave functions. "
            "The scene includes advanced physics equipment and visual aids for teaching."
        )
        result = agent.post_image_tweet(prompt=physics_prompt)

        # For face swap
        portrait_prompt = (
            "A physics professor standing at a modern lecture podium, explaining a concept "
            "with enthusiasm. The background shows a well-equipped physics laboratory with "
            "advanced equipment and scientific diagrams."
        )
        result = agent.post_face_tweet(base_image_prompt=portrait_prompt)

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")


def save_schedule(schedule, filename):
    """Save the schedule to a JSON file for review."""
    with open(filename, "w") as f:
        json.dump(schedule, f, indent=2)
    print(f"\nSchedule saved to {filename}")


if __name__ == "__main__":
    main()
