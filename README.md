# Google OAuth2 with FastAPI Users

This repository provides a Google OAuth2 implementation using the [FastAPI Users](https://github.com/fastapi-users/fastapi-users/) library. It includes CRUD operations for user management and utilizes PostgreSQL as the database, with Alembic for database migrations.

## Features

- Google OAuth Authentication
- CRUD operations for users
- Integration with PostgreSQL database
- Migrations handled with Alembic

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.7+
- PostgreSQL
- Docker (optional, for containerized deployment)

### Running PostgreSQL in Docker

If you want to run PostgreSQL 13 in a Docker container, you can use the following command:

```bash
docker run --name my_postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=osama1122334455! -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres:13
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/osamaaslam86004/google-auth2-fastapi.git
   cd jwt-auth-fastAPI
   ```

## Configure Database Settings
Configure your database settings in the application. The connection URL is:

DATABASE_URL = "postgresql+asyncpg://postgres:osama1122334455!@localhost:5432/mydatabase"

## Database Migrations
Alembic is used for handling database migrations. To create and apply migrations, follow these steps:

- `alembic revision --autogenerate -m "Initial migration`
- `alembic upgrade head`

## Running the Application
To run the FastAPI application, use the following command:

`uvicorn main:app --host 0.0.0.0 --port 8000`

Visit http://localhost:8000/docs to access the interactive API documentation provided by Swagger UI.

### Usage
You can now use the endpoints provided by the FastAPI application to manage users and authenticate them via JWT.

#### Acknowledgments
- FastAPI - The web framework used.
- FastAPI Users - Library for handling user management.
- PostgreSQL - The database used for this project.
- Alembic - For database migrations.