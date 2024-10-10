from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi import Depends, Request
import uuid
from typing import Optional
from user.database_adapter import get_user_db
from fastapi_users.db import SQLAlchemyUserDatabase
from user.models.user_models import User


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = "SECRET"
    verification_token_secret = "SECRET"

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


async def get_user_manager_instance(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
):
    return UserManager(user_db)


# Custom UserManager class
class CustomUserManager(UserManager):
    async def authenticate(self, user: User):
        return await super().authenticate(user)


async def get_custom_user_manager(user_db=Depends(get_user_db)):
    yield CustomUserManager(user_db)
