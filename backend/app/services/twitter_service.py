# backend/app/services/twitter_service.py

import tweepy
from app.core.config import settings

# Authenticate to the Twitter API v2
# We use OAuth 1.0a for this type of user context posting
def get_twitter_client():
    """
    Creates and returns an authenticated Tweepy client.
    """
    client = tweepy.Client(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_API_SECRET,
        access_token=settings.TWITTER_ACCESS_TOKEN,
        access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    return client

def get_twitter_api_v1():
    """
    Creates and returns an authenticated Tweepy API v1.1 object.
    This is needed for posting tweets with Essential tier access.
    """
    auth = tweepy.OAuthHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET
    )
    auth.set_access_token(
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)
    return api

def post_tweet(tweet_text: str) -> bool:
    """
    Posts a tweet to Twitter using v1.1 API (works with Essential tier).

    Args:
        tweet_text: The content of the tweet to post.

    Returns:
        True if successful, False otherwise.
    """
    try:
        # Debug: Print credentials to verify they're loaded
        print(f"DEBUG - API Key loaded: {bool(settings.TWITTER_API_KEY)}")
        print(f"DEBUG - API Secret loaded: {bool(settings.TWITTER_API_SECRET)}")
        print(f"DEBUG - Access Token loaded: {bool(settings.TWITTER_ACCESS_TOKEN)}")
        print(f"DEBUG - Access Token Secret loaded: {bool(settings.TWITTER_ACCESS_TOKEN_SECRET)}")
        
        if not all([settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET, 
                    settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET]):
            print("ERROR: Missing Twitter credentials!")
            return False
        
        # Try v1.1 API first (works with Essential tier)
        api = get_twitter_api_v1()
        status = api.update_status(tweet_text)
        print(f"Successfully posted tweet with ID: {status.id}")
        return True
    except tweepy.TweepyException as e:
        print(f"Error posting to Twitter: {e}")
        print(f"Error response: {e.response if hasattr(e, 'response') else 'N/A'}")
        # If v1.1 fails, could try v2 as fallback
        try:
            print("Trying v2 API...")
            client = get_twitter_client()
            response = client.create_tweet(text=tweet_text)
            print(f"Successfully posted tweet with v2 API. ID: {response.data['id']}")
            return True
        except Exception as e2:
            print(f"v2 API also failed: {e2}")
            return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False