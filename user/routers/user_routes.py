from fastapi import APIRouter, Depends, status
from fastapi_users import models, BaseUserManager
from user.user_manager import get_user_manager
from fastapi import Request
from fastapi_auth.custom_dependency import JWTBearer
from fastapi_auth.utils import get_token_user


user_routers = APIRouter()


@user_routers.get(
    "/protected-route-only-jwt",
    dependencies=[Depends(JWTBearer(token_type="access"))],
)
def protected_route():
    return f"Hello. You are authenticated with a JWT."


@user_routers.delete(
    "/me",
    dependencies=[Depends(JWTBearer(token_type="access"))],
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid token.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The user does not exist.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid token type.",
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
async def delete_own_account(
    payload: dict = Depends(JWTBearer(token_type="access")),
    user_manager_instance: BaseUserManager[models.UP, models.ID] = Depends(
        get_user_manager
    ),
):

    user = await get_token_user(payload, user_manager_instance)

    await user_manager_instance.user_db.delete(user)
    return None
