import tweepy
from typing import Dict, Any, Optional


class TwitterIntegration:
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ):
        """Initialize Twitter API client."""
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    def post_tweet(self, text: str) -> Dict[str, Any]:
        """Post a text-only tweet."""
        try:
            response = self.client.create_tweet(text=text)
            return {
                "status": "success",
                "message": "Tweet posted successfully",
                "tweet_id": response.data["id"],
            }
        except Exception as e:
            return {
                "status": "failed",
                "message": f"Failed to post tweet: {str(e)}",
            }

    def post_tweet_with_media(self, text: str, media_path: str) -> Dict[str, Any]:
        """Post a tweet with media attachment."""
        try:
            print("\nUploading media...")
            # Upload media using v1.1 API
            media = self.api.media_upload(filename=media_path)
            print(f"Media uploaded with ID: {media.media_id}")

            # Post tweet with media using v2 API
            response = self.client.create_tweet(text=text, media_ids=[media.media_id])

            return {
                "status": "success",
                "message": "Tweet with media posted successfully",
                "tweet_id": response.data["id"],
                "media_id": media.media_id,
            }

        except Exception as e:
            print(f"Error posting tweet with media: {str(e)}")
            return {
                "status": "failed",
                "message": f"Failed to post tweet with media: {str(e)}",
            }

    def delete_tweet(self, tweet_id: str) -> Dict[str, Any]:
        """Delete a tweet by ID."""
        try:
            self.client.delete_tweet(id=tweet_id)
            return {
                "status": "success",
                "message": "Tweet deleted successfully",
            }
        except Exception as e:
            return {
                "status": "failed",
                "message": f"Failed to delete tweet: {str(e)}",
            }
