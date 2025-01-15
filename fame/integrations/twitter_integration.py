import tweepy
from typing import Optional, Dict, Any


class TwitterIntegration:
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ):
        """Initialize Twitter API v2 client."""
        # Initialize API v2 client
        self.client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        # Initialize API v1.1 client for media upload
        auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        self.api = tweepy.API(auth)

    def post_tweet(self, text: str) -> Dict[str, Any]:
        """
        Post a text tweet using Twitter API v2.

        Args:
            text: Tweet content

        Returns:
            Dict containing status and response details
        """
        try:
            response = self.client.create_tweet(text=text)

            return {
                "status": "success",
                "tweet_id": response.data["id"],
                "message": "Tweet posted successfully",
            }

        except Exception as e:
            return {
                "status": "failed",
                "message": f"Error posting tweet: {str(e)}",
            }

    def post_image_tweet(
        self, image_path: str, status_text: str = ""
    ) -> Dict[str, Any]:
        """
        Post a tweet with an image using Twitter API v1.1 for media and v2 for tweet.

        Args:
            image_path: Path to image file
            status_text: Optional tweet text

        Returns:
            Dict containing status and response details
        """
        try:
            # Upload media using v1.1 API
            media = self.api.media_upload(filename=image_path)

            # Post tweet with media using v2 API
            response = self.client.create_tweet(
                text=status_text, media_ids=[media.media_id]
            )

            return {
                "status": "success",
                "tweet_id": response.data["id"],
                "media_id": media.media_id,
                "message": "Image tweet posted successfully",
            }

        except Exception as e:
            return {
                "status": "failed",
                "message": f"Error posting image tweet: {str(e)}",
            }

    def reply_to_tweet(
        self, tweet_id: str, text: str, image_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Reply to a tweet, optionally with an image.

        Args:
            tweet_id: ID of tweet to reply to
            text: Reply text
            image_path: Optional path to image file

        Returns:
            Dict containing status and response details
        """
        try:
            media_ids = None
            if image_path:
                media = self.api.media_upload(filename=image_path)
                media_ids = [media.media_id]

            response = self.client.create_tweet(
                text=text, in_reply_to_tweet_id=tweet_id, media_ids=media_ids
            )

            return {
                "status": "success",
                "tweet_id": response.data["id"],
                "reply_to": tweet_id,
                "message": "Reply posted successfully",
            }

        except Exception as e:
            return {
                "status": "failed",
                "message": f"Error posting reply: {str(e)}",
            }

    def retweet(self, tweet_id: str) -> Dict[str, Any]:
        """
        Retweet a tweet using API v2.

        Args:
            tweet_id: ID of tweet to retweet

        Returns:
            Dict containing status and response details
        """
        try:
            response = self.client.retweet(tweet_id)

            return {
                "status": "success",
                "tweet_id": response.data["id"],
                "retweeted_id": tweet_id,
                "message": "Tweet retweeted successfully",
            }

        except Exception as e:
            return {
                "status": "failed",
                "message": f"Error retweeting: {str(e)}",
            }
