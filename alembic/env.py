from __future__ import print_function
from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from database import Base

# from user.models.user_models import OAuthAccount, User
from user.models.user_models import User, OAuthAccount

import logging

logger = logging.getLogger(__name__)

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable here as well.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    This creates an async connection engine and runs migrations online.
    """
    logger.info("Starting online migrations...")
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        logger.info("Connection established. Running migrations...")
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()
    logger.info("Migrations complete.")


def do_run_migrations(connection):
    """Configure the migration context to run migrations."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # Compare column types
        compare_server_default=True,  # Compare server defaults
    )

    with context.begin_transaction():
        context.run_migrations()


# Determine if the context is offline or online, and run the appropriate migration function
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
