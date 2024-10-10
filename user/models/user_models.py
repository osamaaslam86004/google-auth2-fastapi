from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyBaseOAuthAccountTable
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped
from database import Base
import uuid
from typing import List


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable, Base):
    __tablename__ = "oauth_account"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="oauth_accounts")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4()


class User(SQLAlchemyBaseUserTable, Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount",
        lazy="joined",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4()
