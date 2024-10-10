from httpx_oauth.clients.google import GoogleOAuth2
from decouple import config


# Retrieve secrets and expiration times from environment variables
GOOGLE_OAUTH_CLIENT_ID = config("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = config("GOOGLE_OAUTH_CLIENT_SECRET")


google_oauth_client = GoogleOAuth2(
    GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET, name="google"
)
