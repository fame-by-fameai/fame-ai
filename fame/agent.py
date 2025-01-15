from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import os
import random
from typing import Optional, Dict, List, Any
from fame.integrations.replicate_integration import ReplicateIntegration
from fame.integrations.openrouter_integration import OpenRouterIntegration
from fame.integrations.twitter_integration import TwitterIntegration
from fame.core.facets_of_personality import FacetsOfPersonality
from fame.core.abilities_and_knowledge import AbilitiesAndKnowledge
from fame.core.mood_and_emotions import MoodAndEmotions
from .utils.tweet_validator import TweetValidator
from .utils.path_utils import resolve_profile_path
from dotenv import load_dotenv


class Agent:
    def __init__(
        self,
        facets_of_personality: str,
        abilities_knowledge: str,
        mood_emotions: str,
        environment_execution: List[Dict[str, Any]],
        profile_image_path: str = None,
        replicate_models: dict = None,
        openrouter_models: dict = None,
        env_file: str = ".env",
    ):
        """Initialize agent with configuration from environment file."""
        # Load environment variables
        load_dotenv(env_file)

        # Get credentials from environment
        self.x_consumer_key = os.getenv("X_CONSUMER_KEY")
        self.x_consumer_secret = os.getenv("X_CONSUMER_SECRET")
        self.x_access_token = os.getenv("X_ACCESS_TOKEN")
        self.x_access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
        self.replicate_api_key = os.getenv("REPLICATE_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

        # Validate required environment variables
        required_vars = [
            "X_CONSUMER_KEY",
            "X_CONSUMER_SECRET",
            "X_ACCESS_TOKEN",
            "X_ACCESS_TOKEN_SECRET",
            "REPLICATE_API_KEY",
            "OPENROUTER_API_KEY",
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                "Please check your .env file and ensure all required variables are set."
            )

        # Initialize personality components
        self.facets = FacetsOfPersonality(facets_of_personality)
        self.abilities = AbilitiesAndKnowledge(abilities_knowledge)
        self.mood = MoodAndEmotions(mood_emotions)

        # Resolve profile image path
        if profile_image_path:
            resolved_path = resolve_profile_path(profile_image_path)
            if not resolved_path:
                raise ValueError(
                    f"Profile image not found at {profile_image_path}. "
                    "Please provide a valid path relative to the project root "
                    "or an absolute path."
                )
            self.profile_image_path = resolved_path
        else:
            self.profile_image_path = None

        # Initialize integrations with optional custom models
        self.replicate_integration = ReplicateIntegration(
            api_key=self.replicate_api_key, custom_models=replicate_models
        )
        self.openrouter_integration = OpenRouterIntegration(
            api_key=self.openrouter_api_key, custom_models=openrouter_models
        )
        self.twitter_integration = TwitterIntegration(
            consumer_key=self.x_consumer_key,
            consumer_secret=self.x_consumer_secret,
            access_token=self.x_access_token,
            access_token_secret=self.x_access_token_secret,
        )

        # Initialize scheduler only if environment_execution contains schedule info
        self.scheduler = None
        if environment_execution:
            for config in environment_execution:
                if config.get("schedule"):
                    self.scheduler = BackgroundScheduler()
                    self.scheduler.start()
                    self._configure_posting_schedule(config["schedule"])
                    break

    def _configure_posting_schedule(self, schedule_config: Dict[str, Any]):
        """Configure automated posting schedule if provided."""
        if not schedule_config:
            return

        start_time = schedule_config.get("start_time")
        post_frequency = schedule_config.get("post_frequency", "daily")
        posts_per_day = schedule_config.get("posts_per_day", 1)

        if post_frequency == "daily":
            interval = 24 // posts_per_day  # Hours between posts
            if start_time:
                start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            else:
                start_datetime = datetime.now() + timedelta(minutes=1)

            self.scheduler.add_job(
                self._scheduled_post,
                "interval",
                hours=interval,
                start_date=start_datetime,
                id="posting_schedule",
            )

    def _generate_image_prompt(self, for_face_swap: bool = False) -> str:
        """Generate an image prompt based on agent's characteristics."""
        personality = self.facets.get_personality_context()
        abilities = self.abilities.get_knowledge_context()
        emotional_state = self.mood.get_current_emotional_state()

        if for_face_swap:
            # Person-focused prompt for face swapping
            prompt_template = f"""
            Create a professional portrait scene for {personality['traits'][0]}.
            
            Character Details:
            - Identity: {personality.get('human_traits', {}).get('identity', 'person')}
            - Role: {abilities.get('role', 'professional')}
            - Style: {personality.get('human_traits', {}).get('style', 'professional')}
            - Current Mood: {emotional_state['mood']}
            
            Requirements:
            - Natural and professional setting
            - Front-facing pose
            - Well-lit scene
            - Clear facial view
            - Environment matching their profession
            
            Keep the description concise and focused on the portrait setup.
            """
        else:
            # Knowledge and value sharing focused prompt
            primary_field = abilities.get("primary_field", "their field")
            expertise_list = abilities.get("expertise", [])
            expertise = expertise_list[0] if expertise_list else primary_field

            prompt_template = f"""
            Create a concise scene (max 50 words) that teaches or demonstrates knowledge in {primary_field}.
            
            Focus Elements:
            - Key concepts or principles from {expertise}
            - Visual explanations or demonstrations
            - Professional tools or equipment
            - Data visualizations or diagrams
            
            Requirements:
            - No people or human figures
            - Pure focus on knowledge/concept visualization
            - Clear, educational composition
            - Professional and engaging visual style
            - High-quality technical details
            
            The scene should effectively communicate expertise while being visually engaging.
            """

        response = self.openrouter_integration.generate_text(
            prompt_template, model_type="text_generation"
        )

        return (
            response.strip()
            if response
            else f"A professional visualization demonstrating {primary_field} concepts"
        )

    def post_image_tweet(
        self, prompt: Optional[str] = None, tweet_text: Optional[str] = None
    ) -> Dict[str, str]:
        """Post a regular image tweet using AI image generation."""
        # Get agent's full context
        abilities = self.abilities.get_knowledge_context()
        personality = self.facets.get_personality_context()
        mood = self.mood.get_current_emotional_state()

        if not prompt:
            # Get background information
            role = abilities.get("role", "professional")
            primary_field = abilities.get("primary_field", "")

            # Generate abstract visual concept
            visual_prompt = f"""
            Create an abstract, conceptual visualization related to {primary_field}.
            
            Style Elements:
            - Clean, minimalist design
            - Professional data visualization
            - Abstract geometric patterns
            - Technical diagrams or schematics
            - Modern, sleek aesthetics
            
            Requirements:
            - No text overlays
            - No human figures
            - Pure visual representation
            - Professional color scheme
            
            The scene should be visually engaging but abstract enough to represent any concept.
            """

            image_prompt = self._generate_image_prompt(for_face_swap=False)
        else:
            image_prompt = prompt

        # Generate image
        image_path = self.replicate_integration.generate_image(image_prompt)

        if not image_path:
            return {"status": "failed", "message": "Image generation failed"}

        try:
            if tweet_text is None:
                # Get personality traits
                communication_style = personality.get("communication_style", "direct")
                current_projects = abilities.get("projects", [])
                companies = abilities.get("companies", [])

                # Generate tweet with personality-specific style
                tweet_text = (
                    self.openrouter_integration.generate_text(
                        f"""
                        Write a tweet about {current_projects[0] if current_projects else 'innovation'}, considering:

                        Style:
                        - Direct and bold statements
                        - Mix of technical and visionary content
                        - Occasional memes or humor
                        - Use of emojis for emphasis
                        - Short, impactful sentences
                        
                        Context:
                        - Companies: {', '.join([c['name'] for c in companies])}
                        - Current focus: {current_projects[0] if current_projects else 'technology'}
                        - Mood: {mood.get('mood', 'enthusiastic')}
                        
                        Requirements:
                        - Be provocative yet insightful
                        - Include technical details
                        - Add future vision
                        - Keep under 280 chars
                        - Don't mention images
                        
                        Write in a bold, visionary style with occasional humor.
                        """
                    )
                    or f"The future of {current_projects[0] if current_projects else 'technology'} is now! 🚀"
                )

            # Post tweet
            result = self.twitter_integration.post_image_tweet(
                image_path=image_path,
                status_text=tweet_text,
            )

            # Cleanup
            os.remove(image_path)
            return {
                "status": "success" if result else "failed",
                "message": "Image tweet posted successfully",
            }

        except Exception as e:
            if os.path.exists(image_path):
                os.remove(image_path)
            return {"status": "failed", "message": f"Error posting tweet: {str(e)}"}

    def _generate_base_image_prompt(self) -> str:
        """
        Generate a base image prompt that's suitable for face swapping.
        Incorporates agent's personality while ensuring good face swap results.
        """
        # Get personality context for better prompt generation
        personality = self.facets.get_personality_context()
        emotional_state = self.mood.get_current_emotional_state()

        # Extract key characteristics
        traits = personality.get("traits", [])
        interests = personality.get("interests", [])
        main_trait = traits[0] if traits else "person"

        # Extract or infer human characteristics
        human_traits = self._extract_human_traits(personality)

        # Create a contextual scene based on agent's traits
        scene_prompt = self.openrouter_integration.generate_text(
            prompt=f"""
            Create a scene description for a photo of {main_trait}.
            
            Character Details:
            - Identity: {human_traits['identity']}
            - Age Group: {human_traits['age_group']}
            - Appearance: {human_traits['appearance']}
            - Style: {human_traits['style']}
            
            Personality Context:
            - Core Traits: {', '.join(traits)}
            - Main Interests: {', '.join(interests)}
            - Current Mood: {emotional_state['mood']}
            - Primary Activity: {interests[0] if interests else 'daily life'}
            
            Requirements:
            - Create a natural, realistic scene
            - Show a single person in their element
            - Include relevant environment details
            - Reflect their interests and current mood
            - Keep it under 30 words
            - Focus on the setting and activity
            - Ensure scene matches their identity and age group
            
            The scene should feel authentic to this person's character and background.
            """,
            model_type="text_generation",
        )

        if not scene_prompt:
            # Personality-aware fallback prompt
            scene_prompt = (
                f"A {human_traits['age_group']} {human_traits['identity']} "
                f"expressing {main_trait} in their natural environment"
            )

        # Combine with system requirements for good face swapping
        # Note: Keep technical requirements separate from personality-based content
        enhanced_prompt = (
            f"{scene_prompt}, "
            f"{human_traits['appearance']}, {human_traits['style']}, "
            "portrait style, front facing, clear face view, "
            "professional lighting, sharp focus, high detail facial features, "
            "professional photography, centered composition, 8k uhd, "
            "natural skin texture, realistic features"
        )

        return enhanced_prompt

    def _extract_human_traits(self, personality: Dict) -> Dict[str, str]:
        """
        Extract or infer human characteristics from personality description.
        """
        description = " ".join(personality.get("traits", []))
        description = description.lower()

        # Default traits
        traits = {
            "identity": "person",
            "age_group": "young adult",
            "appearance": "natural looking",
            "style": "casual",
        }

        # Gender/Identity inference
        gender_indicators = {
            "woman": ["woman", "girl", "female", "she", "her"],
            "man": ["man", "boy", "male", "he", "his"],
            # Add other identities as needed
        }

        for identity, indicators in gender_indicators.items():
            if any(indicator in description for indicator in indicators):
                traits["identity"] = identity
                break

        # Age group inference
        age_indicators = {
            "teenager": ["teen", "teenage", "adolescent", "high school"],
            "young adult": ["young", "college", "20s"],
            "adult": ["adult", "professional", "working"],
            # Add other age groups as needed
        }

        for age_group, indicators in age_indicators.items():
            if any(indicator in description for indicator in indicators):
                traits["age_group"] = age_group
                break

        # Style inference
        style_indicators = {
            "professional": ["business", "formal", "professional"],
            "artistic": ["creative", "artistic", "expressive"],
            "athletic": ["sporty", "athletic", "active"],
            "elegant": ["elegant", "graceful", "sophisticated"],
            # Add other styles as needed
        }

        for style, indicators in style_indicators.items():
            if any(indicator in description for indicator in indicators):
                traits["style"] = style
                break

        # Appearance inference based on profession/interests
        if "dancer" in description or "ballet" in description:
            traits["appearance"] = "graceful posture, athletic build"
        elif "athlete" in description or "sports" in description:
            traits["appearance"] = "athletic build, fit appearance"
        elif "professional" in description or "business" in description:
            traits["appearance"] = "well-groomed, professional appearance"

        return traits

    def post_face_tweet(
        self, base_image_prompt: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Post a tweet with the agent's face swapped onto a generated image.

        Args:
            base_image_prompt: Optional prompt for the base image. If not provided,
                             will generate one based on agent's personality.
        """
        if not self.profile_image_path:
            return {
                "status": "failed",
                "message": "No profile image provided for face swapping",
            }

        try:
            # Generate or use provided prompt
            if base_image_prompt is None:
                base_image_prompt = self._generate_image_prompt(for_face_swap=True)
            else:
                # Enhance user-provided prompt with system requirements
                base_image_prompt = (
                    f"{base_image_prompt}, "
                    "single person, front facing portrait, clear face view, "
                    "professional studio lighting, sharp focus, high detail facial features"
                )

            # Generate image and perform face swap
            base_image_path, swapped_image_path = (
                self.replicate_integration.generate_and_swap(
                    prompt=base_image_prompt,
                    face_image_path=self.profile_image_path,
                )
            )

            if not swapped_image_path:
                return {"status": "failed", "message": "Face swap failed"}

            try:
                # Generate tweet text based on the image and agent's personality
                tweet_text = (
                    self.openrouter_integration.generate_text(
                        f"Write a tweet caption for a photo where {self.facets.core_traits[0]} "
                        f"is {base_image_prompt.split(',')[0].lower()}. "
                        f"Current mood: {self.mood.current_mood}"
                    )
                    or "Living my best life! ✨"
                )

                result = self.twitter_integration.post_image_tweet(
                    image_path=swapped_image_path,
                    status_text=tweet_text,
                )

                # Cleanup temporary files
                for path in [base_image_path, swapped_image_path]:
                    if path and os.path.exists(path):
                        os.remove(path)

                return {
                    "status": "success" if result else "failed",
                    "message": "Face-swapped image posted successfully",
                }

            except Exception as e:
                # Cleanup on error
                for path in [base_image_path, swapped_image_path]:
                    if path and os.path.exists(path):
                        os.remove(path)
                return {"status": "failed", "message": f"Error posting tweet: {str(e)}"}

        except Exception as e:
            return {
                "status": "failed",
                "message": f"Error in face swap process: {str(e)}",
            }

    def _scheduled_post(self):
        """Handle a scheduled post."""
        # Randomly choose between text, regular image, or face-swapped image
        post_type = random.choice(["text", "image", "face"])

        if post_type == "text":
            self.post_text_tweet(use_llm=True)
        elif post_type == "image":
            self.post_image_tweet()  # Will generate appropriate prompt
        elif post_type == "face" and self.profile_image_path:
            self.post_face_tweet()  # Will generate appropriate prompt

    def set_replicate_model(
        self, model_type: str, model_id: str, default_params: dict = None
    ):
        """
        Set or update a Replicate model configuration.

        Args:
            model_type: Type of model (e.g., "image_generation", "face_swap")
            model_id: Replicate model ID
            default_params: Optional default parameters for the model
        """
        self.replicate_integration.set_model(model_type, model_id, default_params)

    def set_openrouter_model(
        self, model_type: str, model_id: str, default_params: dict = None
    ):
        """
        Set or update an OpenRouter model configuration.

        Args:
            model_type: Type of model (e.g., "text_generation", "chat")
            model_id: OpenRouter model ID
            default_params: Optional default parameters for the model
        """
        self.openrouter_integration.set_model(model_type, model_id, default_params)

    def _generate_tweet_content(
        self, instruction: str = None, max_attempts: int = 3
    ) -> Optional[str]:
        """
        Generate tweet content using LLM with validation and regeneration.

        Args:
            instruction: Optional high-level instruction for tweet content
            max_attempts: Maximum number of generation attempts

        Returns:
            Valid tweet content or None if failed
        """
        base_prompt = self._create_tweet_prompt(instruction)

        for attempt in range(max_attempts):
            # Generate tweet content
            content = self.openrouter_integration.generate_text(
                prompt=base_prompt, model_type="text_generation"
            )

            if not content:
                continue

            # Validate the generated content
            is_valid, details = TweetValidator.validate_tweet(content)

            if is_valid:
                return content

            # If invalid, try to fix with more specific prompt
            fix_prompt = self._create_fix_tweet_prompt(content, details)
            content = self.openrouter_integration.generate_text(
                prompt=fix_prompt, model_type="text_generation"
            )

            # Validate the fixed content
            is_valid, details = TweetValidator.validate_tweet(content)
            if is_valid:
                return content

        return None

    def _create_tweet_prompt(self, instruction: str = None) -> str:
        """Create a prompt for tweet generation."""
        personality_context = self.facets.get_personality_context()
        emotional_state = self.mood.get_current_emotional_state()

        base_prompt = f"""
        You are writing a tweet as {personality_context['traits'][0]}.
        Current mood: {emotional_state['mood']} (intensity: {emotional_state['intensity']})
        Interests: {', '.join(personality_context['interests'])}
        Communication style: {personality_context['current_style']}

        Rules for the tweet:
        1. Must be under 280 characters
        2. Focus on sharing knowledge or value
        3. Be educational and informative
        4. Include practical insights
        5. Use at most 2 relevant hashtags
        6. Keep emojis minimal (0-2)
        7. Single tweet only (no thread)
        8. No character counts or metadata

        {f'Instruction: {instruction}' if instruction else 'Share a valuable insight about your expertise.'}

        Write only the tweet text, without any additional information:
        """

        return base_prompt

    def _create_fix_tweet_prompt(
        self, original_content: str, validation_details: Dict
    ) -> str:
        """Create a prompt to fix invalid tweet content."""
        issues = "\n".join(validation_details["issues"])
        suggestions = "\n".join(validation_details["suggestions"])

        fix_prompt = f"""
        The following tweet needs to be fixed:
        "{original_content}"

        Issues:
        {issues}

        Suggestions:
        {suggestions}

        Please rewrite the tweet to fix these issues while maintaining the same message and tone.
        Must be under 280 characters.

        Fixed tweet:
        """

        return fix_prompt

    def post_tweet(self, instruction: Optional[str] = None) -> Dict[str, str]:
        """
        Generate and post a tweet.

        Args:
            instruction: Optional high-level instruction for tweet content

        Returns:
            Dict containing status and response details
        """
        # Generate tweet content
        content = self._generate_tweet_content(instruction)

        if not content:
            return {
                "status": "failed",
                "message": "Failed to generate valid tweet content",
            }

        # Post the tweet
        return self.twitter_integration.post_tweet(content)

    def draft_scheduled_posts(
        self, posts_per_day: int, interval: str, duration: int
    ) -> List[Dict[str, Any]]:
        """
        Draft a schedule of posts for review.

        Args:
            posts_per_day: Number of posts per interval
            interval: Time interval ('day', 'week', 'month')
            duration: Number of intervals to schedule

        Returns:
            List of draft posts with content, type, and timing
        """
        total_posts = posts_per_day * duration
        draft_posts = []

        # Get personality context for content generation
        personality = self.facets.get_personality_context()
        interests = personality.get("interests", [])
        human_traits = personality.get("human_traits", {})

        # Define post types and weights based on personality
        post_types = {
            "text": 0.4,  # Regular text updates
            "image": 0.3,  # AI-generated images
            "face": 0.3,  # Face-swapped images
        }

        # Generate diverse topics based on interests and traits
        base_topics = [f"Updates about {interest}" for interest in interests] + [
            "Daily activities",
            "Achievements and milestones",
            "Tips and advice",
            "Behind the scenes",
            "Progress updates",
            "Inspirational moments",
            "Learning experiences",
        ]

        # Ensure we have enough diverse topics
        topics = base_topics * (total_posts // len(base_topics) + 1)
        random.shuffle(topics)

        for day in range(duration):
            for post in range(posts_per_day):
                # Select post type based on weights
                post_type = random.choices(
                    list(post_types.keys()), weights=list(post_types.values())
                )[0]

                # Get current topic
                topic_index = day * posts_per_day + post
                current_topic = topics[topic_index]

                # Generate content based on type and topic
                draft_content = self._generate_draft_content(
                    post_type=post_type, topic=current_topic, personality=personality
                )

                # Create draft post entry
                draft_post = {
                    "day": day + 1,
                    "post_number": post + 1,
                    "post_type": post_type,
                    "topic": current_topic,
                    "content": draft_content,
                    "timing": self._suggest_post_timing(
                        day=day,
                        post_number=post,
                        posts_per_day=posts_per_day,
                        personality=personality,
                    ),
                }

                draft_posts.append(draft_post)

        return draft_posts

    def _generate_draft_content(
        self, post_type: str, topic: str, personality: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate draft content for a specific post type and topic."""
        # Get emoji preferences
        emoji_style = self.mood.emoji_style
        emoji_note = (
            f"Use {self.mood.get_emoji_count()} emoji(s) in {emoji_style['style']} style"
            if self.mood.should_use_emoji()
            else "Do not use emojis"
        )

        if post_type == "text":
            prompt = f"""
            Write a tweet about {topic}.
            Personality: {personality['traits'][0]}
            Style: {personality['current_style']}
            Emoji usage: {emoji_note}
            Keep it natural and authentic to the character.
            """
            content = {
                "text": self.openrouter_integration.generate_text(prompt)
                or f"Draft tweet about {topic}"
            }

        elif post_type == "image":
            # Should be knowledge/value focused instead of personality focused
            prompt = f"""
            Create a visual demonstration or explanation about {topic}.
            Focus on:
            - Key concepts or principles
            - Visual explanations or diagrams
            - Professional tools or techniques
            - Educational value
            Keep it under 50 words and focus on knowledge sharing.
            """
            image_prompt = self.openrouter_integration.generate_text(prompt)
            content = {
                "image_prompt": image_prompt,
                "text": f"Educational insight about {topic}",
            }

        elif post_type == "face":
            # Generate face swap concept
            prompt = f"""
            Describe a scene related to {topic} where {personality['traits'][0]} might appear.
            Focus on the setting and activity.
            Keep it under 50 words.
            """
            scene_prompt = self.openrouter_integration.generate_text(prompt)
            content = {
                "base_image_prompt": scene_prompt,
                "text": f"Draft caption about {topic}",
            }

        return content

    def _suggest_post_timing(
        self,
        day: int,
        post_number: int,
        posts_per_day: int,
        personality: Dict[str, Any],
    ) -> str:
        """Suggest appropriate timing for a post based on personality and schedule."""

        # Base time range (assuming 16 hour day from 6AM to 10PM)
        day_start = 6  # 6 AM
        day_end = 22  # 10 PM
        available_hours = day_end - day_start

        # Calculate time slot for this post
        slot_duration = available_hours / posts_per_day
        post_hour = day_start + (slot_duration * post_number)

        # Add some randomness within the slot
        post_hour += random.uniform(0, slot_duration * 0.5)
        post_hour = min(day_end - 1, max(day_start, post_hour))

        # Format time
        hour = int(post_hour)
        minute = int((post_hour % 1) * 60)
        ampm = "AM" if hour < 12 else "PM"
        if hour > 12:
            hour -= 12

        return f"Day {day + 1} at {hour:02d}:{minute:02d} {ampm}"
