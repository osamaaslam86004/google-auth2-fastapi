from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_auth.config import (
    refresh_auth_backend,
    access_auth_backend,
    get_refresh_jwt_strategy,
)
from user.user_manager import get_user_manager, UserManager
from fastapi_auth.schemas.jwt_auth_schema import TokenResponse, AccessTokenResponse
from fastapi_auth.custom_dependency import JWTBearer, RefreshJWTBearer
from fastapi_auth.utils import get_token_user


custom_jwt_auth_router = APIRouter()


@custom_jwt_auth_router.post(
    "/jwt/login",
    responses={
        status.HTTP_200_OK: {
            "description": "Access token and refresh token created.",
            "model": TokenResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials or inactive user.",
        },
    },
)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager_instance: UserManager = Depends(get_user_manager),
):
    # Use the 'username' field, which contains the email in this case
    user = await user_manager_instance.authenticate(credentials)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create an access token and refresh token
    access_token = await access_auth_backend.get_strategy().write_token(user)
    refresh_token = await refresh_auth_backend.get_strategy().write_token(user)

    return {"access_token": access_token, "refresh_token": refresh_token}


@custom_jwt_auth_router.post(
    "/jwt/refresh",
    description="refresh token in header with Authorization Beaer is required",
    responses={
        status.HTTP_200_OK: {
            "description": "New access token generated",
            "model": AccessTokenResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid refresh token.",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid authorization header format / Refresh token not provided.",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error - Check request format.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["header", "authorization"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    }
                },
            },
        },
    },
)
async def refresh_access_token(
    refresh_token: dict = Depends(RefreshJWTBearer(token_type="refresh")),
    user_manager_instance: UserManager = Depends(get_user_manager),
):

    # Verify the refresh token
    refresh_strategy = get_refresh_jwt_strategy()
    try:
        # Use the strategy to read and validate the refresh token
        user = await refresh_strategy.read_token(refresh_token, user_manager_instance)

        # Issue a new access token
        access_token = await access_auth_backend.get_strategy().write_token(user)
        return {"access_token": access_token}

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid refresh token: {str(e)}")


# Define the route that uses this dependency for token verification
@custom_jwt_auth_router.get(
    "/jwt/verify",
    responses={
        status.HTTP_200_OK: {
            "description": "Token is valid",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid token type.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid token.",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid authentication scheme / Authorization token not provided",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error - Check request format.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["header", "authorization"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    }
                },
            },
        },
    },
)
async def verify_access_token(
    payload: dict = Depends(JWTBearer(token_type="access")),
    user_manager_instance: UserManager = Depends(get_user_manager),
):

    user = await get_token_user(payload, user_manager_instance)

    # Return success if everything is valid
    return {"message": "Token is valid"}
