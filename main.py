from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import AsyncSessionLocal, engine
from sqlalchemy import text
from contextlib import asynccontextmanager
from fastapi_utils.tasks import repeat_every
from fastapi_auth.auth import fastapi_users
from fastapi_auth.routers.auth_routes import custom_jwt_auth_router
from user.routers.user_routes import user_routers
from user.config import google_oauth_client
from fastapi_auth.config import access_auth_backend
from decouple import config
from user.schemas.user_schemas import UserCreate, UserDB

DATABASE_PING = config("DATABASE_PING")
GOOGLE_ROUTER_SECRET_KEY = config("GOOGLE_ROUTER_SECRET_KEY")

import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


CORS_ALLOWED_ORIGINS = [
    "https://music-player-ui-ux.vercel.app",
    "http://127.0.0.1:60640",
    "https://osama11111.pythonanywhere.com",
    "https://osamaaslam.pythonanywhere.com",
    "https://web.postman.co",
    "https://diverse-intense-whippet.ngrok-free.app",
    "http://127.0.0.1:5500",
    "https://resume-builder-integrated-with-resume-api.vercel.app",
    "https://resume-builder-pwa.vercel.app/",
]


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
    # expose_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup task: keep database connection alive
    logger.info("Starting up and initiating keep-alive task.")

    # Define the keep-alive task
    @repeat_every(seconds=int(DATABASE_PING))  # Runs every 5 seconds
    async def keep_db_alive():
        try:
            async with AsyncSessionLocal() as session:
                await session.execute(text("SELECT 1"))
                logger.info("Keep-alive query executed successfully.")
        except Exception as e:
            logger.error(f"Error executing keep-alive query: {e}")

    # Startup tasks before yielding control to the app
    await keep_db_alive()

    yield

    # Shutdown tasks (if any)
    logger.info("Shutting down.")
    await engine.dispose()
    # Cleanup tasks go here if necessary


# Set lifespan context in the FastAPI app
app = FastAPI(lifespan=lifespan)


app.include_router(
    fastapi_users.get_register_router(UserDB, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client, access_auth_backend, GOOGLE_ROUTER_SECRET_KEY
    ),
    prefix="/auth/google",
    tags=["auth"],
)


app.include_router(custom_jwt_auth_router, prefix="/auth", tags=["auth"])

app.include_router(user_routers, prefix="/user", tags=["user"])


@app.get("/methods", tags=["debug"])
async def get_routes():
    return [
        {"path": route.path, "name": route.name, "methods": list(route.methods)}
        for route in app.routes
    ]


@app.get("/routes", tags=["debug"])
async def get_routes():
    return [
        {
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods),
            # Safely get dependencies if they exist, otherwise default to None
            "dependencies": getattr(route, "dependencies", None),
        }
        for route in app.routes
    ]


# route for root / homepage
@app.get("/")
async def read_root():
    return {"Hello": "World"}
