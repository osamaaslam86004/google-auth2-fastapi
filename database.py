from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession


# import asyncio
import logging
from sqlalchemy.orm import declarative_base

# import ssl

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)  # Logs all SQL queries


DATABASE_URL = (
    "postgresql+asyncpg://postgres:osama1122334455!@localhost:5432/mydatabase"
)


# Create the database engine
engine = create_async_engine(
    DATABASE_URL,
    # connect_args={"ssl": {}},  # Pass the SSL context to the connection or use default
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,  # Adjust timeout to wait for a connection from the pool
    pool_recycle=3600,  # Recycle connections every hour
)


# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Dependency to get the database session in FastAPI routes with retry logic
async def get_db():
    try:
        async with AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    except OperationalError as e:
        logging.error(f"Database connection failed: {e}. Retrying in 5 seconds...")


# Create a base class for your models
Base = declarative_base()
