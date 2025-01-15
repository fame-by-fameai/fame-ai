from fame.agent import Agent
from pathlib import Path
import json
from pprint import pprint


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


def test_draft_schedule():
    """Test the draft schedule functionality with different configurations."""
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
        # Test 1: Generate a week of daily posts
        print("\n=== Testing One Week Schedule (1 post per day) ===")
        weekly_schedule = agent.draft_scheduled_posts(
            posts_per_day=1, interval="day", duration=7
        )
        save_schedule(weekly_schedule, "weekly_schedule.json")
        print_schedule_summary(weekly_schedule)

        # Test 2: Generate a busy day schedule
        print("\n=== Testing Busy Day Schedule (3 posts) ===")
        daily_schedule = agent.draft_scheduled_posts(
            posts_per_day=3, interval="day", duration=1
        )
        save_schedule(daily_schedule, "daily_schedule.json")
        print_schedule_summary(daily_schedule)

        # Test 3: Generate individual content types
        print("\n=== Testing Individual Content Generation ===")
        personality = agent.facets.get_personality_context()

        print("\nText Post Example:")
        text_content = agent._generate_draft_content(
            post_type="text",
            topic="Dance practice achievements",
            personality=personality,
        )
        pprint(text_content)

        print("\nImage Post Example:")
        image_content = agent._generate_draft_content(
            post_type="image",
            topic="Ballet performance preparation",
            personality=personality,
        )
        pprint(image_content)

        print("\nFace Swap Post Example:")
        face_content = agent._generate_draft_content(
            post_type="face", topic="Dance studio session", personality=personality
        )
        pprint(face_content)

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")


def save_schedule(schedule, filename):
    """Save the schedule to a JSON file for review."""
    with open(filename, "w") as f:
        json.dump(schedule, f, indent=2)
    print(f"\nSchedule saved to {filename}")


def print_schedule_summary(schedule):
    """Print a summary of the schedule."""
    print(f"\nTotal posts planned: {len(schedule)}")

    # Count post types
    post_types = {}
    for post in schedule:
        post_type = post["post_type"]
        post_types[post_type] = post_types.get(post_type, 0) + 1

    print("\nPost type distribution:")
    for post_type, count in post_types.items():
        print(f"- {post_type}: {count} posts")

    # Print first post as example
    print("\nExample post:")
    pprint(schedule[0])


if __name__ == "__main__":
    test_draft_schedule()
