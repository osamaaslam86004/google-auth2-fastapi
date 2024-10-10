from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from user.models.user_models import User
from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from user.models.user_models import User, OAuthAccount


# Modify get_user_db to use the get_db dependency
async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)
