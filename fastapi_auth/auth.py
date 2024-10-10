# from main import app
from fastapi_users import FastAPIUsers
from user.user_manager import get_user_manager
from fastapi_auth.config import access_auth_backend, refresh_auth_backend
from user.models.user_models import User
import uuid


# Create a FastAPIUsers instance with both access and refresh backends
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [
        access_auth_backend,
        refresh_auth_backend,
    ],
)


get_current_active_user = fastapi_users.current_user(active=True)
