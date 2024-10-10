from fastapi_users.authentication import AuthenticationBackend
from fastapi_auth.utils import CustomJWTStrategy
from fastapi_users.authentication.transport import BearerTransport
from decouple import config
from pydantic import SecretStr
from fastapi.security import OAuth2PasswordBearer


# Retrieve secrets and expiration times from environment variables
ACCESS_TOKEN_SECRET_KEY = config("ACCESS_TOKEN_SECRET_KEY")
REFRESH_TOKEN_SECRET_KEY = config("REFRESH_TOKEN_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_SECONDS = config("ACCESS_TOKEN_EXPIRE_SECONDS", cast=int)
REFRESH_TOKEN_EXPIRE_SECONDS = config("REFRESH_TOKEN_EXPIRE_SECONDS", cast=int)

# Define a transport for the access token (Bearer)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


# Create the JWT strategy for access tokens
def get_access_jwt_strategy() -> CustomJWTStrategy:
    return CustomJWTStrategy(
        secret=SecretStr(
            ACCESS_TOKEN_SECRET_KEY
        ),  # Use SecretStr for enhanced security
        lifetime_seconds=ACCESS_TOKEN_EXPIRE_SECONDS,
        token_type="access",  # Specify it's for access tokens
    )


# Create the JWT strategy for refresh tokens
def get_refresh_jwt_strategy() -> CustomJWTStrategy:
    return CustomJWTStrategy(
        secret=SecretStr(
            REFRESH_TOKEN_SECRET_KEY
        ),  # Use SecretStr for enhanced security
        lifetime_seconds=REFRESH_TOKEN_EXPIRE_SECONDS,
        token_type="refresh",  # Specify it's for refresh tokens
    )


# Create the authentication backend for access token
access_auth_backend = AuthenticationBackend(
    name="jwt-access", transport=bearer_transport, get_strategy=get_access_jwt_strategy
)

# Create the authentication backend for refresh token
refresh_auth_backend = AuthenticationBackend(
    name="jwt-refresh",
    transport=bearer_transport,
    get_strategy=get_refresh_jwt_strategy,
)
