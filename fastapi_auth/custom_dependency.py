from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from typing import Optional
from fastapi_users.jwt import decode_jwt, _get_secret_value
from user.database_adapter import get_user_db
from decouple import config
from pydantic import SecretStr

ACCESS_TOKEN_SECRET_KEY = SecretStr(config("ACCESS_TOKEN_SECRET_KEY"))
REFRESH_TOKEN_SECRET_KEY = SecretStr(config("REFRESH_TOKEN_SECRET_KEY"))


class JWTBearer(HTTPBearer):
    def __init__(self, token_type: Optional[str] = "access", auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.token_type = token_type

    async def __call__(self, request: Request, db: AsyncSession = Depends(get_user_db)):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            # Decode and verify the token
            token_data = await self.decode_token(credentials.credentials)

            # Check the token type
            if token_data.get("token_type") != self.token_type:
                raise HTTPException(status_code=400, detail="Invalid token type")

            # Check if the token is expired
            if self.token_expired(token_data):
                raise HTTPException(
                    status_code=401,
                    detail=f"{self.token_type.capitalize()} token expired",
                )

            return token_data

        raise HTTPException(status_code=403, detail="Authorization token not provided.")

    async def decode_token(self, token: str):

        try:
            return decode_jwt(
                token,
                secret=_get_secret_value(ACCESS_TOKEN_SECRET_KEY),
                algorithms="HS256",
                audience=["fastapi-users:auth"],
            )
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    def token_expired(self, token_data: dict) -> bool:
        # Get the expiration timestamp (exp)
        exp = datetime.fromtimestamp(token_data.get("exp"), tz=timezone.utc)
        now = datetime.now(timezone.utc)
        # Check if the token has expired
        return exp < now


class RefreshJWTBearer(HTTPBearer):
    def __init__(self, token_type: Optional[str] = "refresh", auto_error: bool = True):
        super(RefreshJWTBearer, self).__init__(auto_error=auto_error)
        self.token_type = token_type

    async def __call__(self, request: Request, db: AsyncSession = Depends(get_user_db)):
        credentials: HTTPAuthorizationCredentials = await super(
            RefreshJWTBearer, self
        ).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            # Decode and verify the token
            token_data = await self.decode_token(credentials.credentials)

            # Check the token type
            if token_data.get("token_type") != self.token_type:
                raise HTTPException(status_code=400, detail="Invalid token type")

            # Check if the token is expired
            if self.token_expired(token_data):
                raise HTTPException(
                    status_code=401,
                    detail=f"{self.token_type.capitalize()} token expired",
                )

            return credentials.credentials

        raise HTTPException(status_code=403, detail="Authorization token not provided.")

    async def decode_token(self, token: str):

        try:
            return decode_jwt(
                token,
                secret=_get_secret_value(REFRESH_TOKEN_SECRET_KEY),
                algorithms="HS256",
                audience=["fastapi-users:auth"],
            )
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    def token_expired(self, token_data: dict) -> bool:
        # Get the expiration timestamp (exp)
        exp = datetime.fromtimestamp(token_data.get("exp"), tz=timezone.utc)
        now = datetime.now(timezone.utc)
        # Check if the token has expired
        return exp < now
