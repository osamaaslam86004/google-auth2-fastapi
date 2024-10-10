from fastapi_users.jwt import generate_jwt
from fastapi_users.authentication.strategy.jwt import JWTStrategy
from fastapi_users import models
from typing import Optional, List
from fastapi_users.jwt import SecretType
from fastapi import HTTPException
from user.user_manager import UserManager


class CustomJWTStrategy(JWTStrategy):
    def __init__(
        self,
        secret: SecretType,
        lifetime_seconds: Optional[int],
        token_audience: List[str] = ["fastapi-users:auth"],
        algorithm: str = "HS256",
        public_key: Optional[SecretType] = None,
        token_type: str = "access",
    ):
        super().__init__(
            secret, lifetime_seconds, token_audience, algorithm, public_key
        )
        self.token_type = token_type

        # Ensure token_type is valid
        if self.token_type not in ["access", "refresh"]:
            raise ValueError("Invalid token type. Must be 'access' or 'refresh'.")

    async def write_token(self, user: models.UP) -> str:
        # Include 'token_type' in the token payload from the init attribute
        data = {
            "sub": str(user.id),  # User ID
            "aud": self.token_audience,  # Audience
            "token_type": self.token_type,  # Use token_type from the instance
        }

        # Generate the JWT with the custom payload
        return generate_jwt(
            data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm
        )


async def get_token_user(payload: dict, user_manager_instance: UserManager):
    # Get user from the token payload
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Fetch the user from the database using the user manager
    try:
        user = await user_manager_instance.get(user_id)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user
