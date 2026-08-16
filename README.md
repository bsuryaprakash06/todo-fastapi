# Todo FastAPI

A production-ready RESTful API for managing tasks built with FastAPI, PostgreSQL, and Supabase Authentication. The project features a layered architecture (Route → Service → Repository → Database), request validation with Pydantic, and multi-container orchestration using Docker Compose.

## Features

- **Authentication**: JWT-based Bearer Authentication integrated with Supabase Auth.
- **Task Management**: Complete CRUD operations for tasks.
- **Advanced Querying**: Search by keyword, filter by status, and sort alphabetically.
- **Statistics**: Task count statistics endpoint.
- **Validation**: Strict request and response validation using Pydantic.
- **Architecture**: Decoupled layers separating business logic from HTTP and database concerns.
- **Containerization**: Automatic database table creation, seeding, and persistent storage via Docker Compose.
- **Documentation**: Interactive Swagger UI with Bearer Authentication lock capabilities.

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Authentication**: Supabase (JWT)
- **Database**: PostgreSQL 16 (Alpine)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Containerization**: Docker & Docker Compose

## Architecture Overview

Supabase handles user accounts and issues JWTs. FastAPI receives the requests, verifies the tokens using a reusable dependency, and handles business logic. Data is stored in PostgreSQL.

```text
       ┌──────────────┐
       │   Supabase   │
       │     Auth     │
       └──────┬───────┘
              │ JWT / User
              ▼
┌──────────────┐   ┌─────────────┐
│    Client    │──►│   FastAPI   │
│ Swagger/Curl │   │             │
└──────────────┘   └──────┬──────┘
                          │
             ┌────────────┴────────────┐
             │                         │
      Auth Dependency            Public Routes
             │
             ▼
      Protected Routes
             │
             ▼
       Task Services
             │
             ▼
        Repository
             │
             ▼
        PostgreSQL
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bsuryaprakash06/todo-fastapi.git
   cd todo-fastapi
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the root of the project with the following structure:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tasks
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@db:5432/tasks

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-client-key
```

Make sure to replace `SUPABASE_URL` and `SUPABASE_KEY` with your actual Supabase project credentials.

## Running the Application

### Using Docker Compose (Recommended)

1. Start the services:
   ```bash
   docker compose up --build
   ```

2. The API will be available at:
   - API Root: `http://127.0.0.1:8000`
   - Interactive Swagger Docs: `http://127.0.0.1:8000/docs`

### Local Development (Without Docker)

If you have a local PostgreSQL instance running:
```bash
uvicorn app.main:app --reload
```

## Authentication Flow

1. User submits `email` and `password` to `/auth/signup`.
2. User submits the same credentials to `/auth/login` to receive an `access_token`.
3. The client includes this token in the `Authorization` header as `Bearer <token>` for protected routes.
4. FastAPI validates the token against Supabase via the `get_current_user` dependency.
5. If valid, access is granted. If missing or invalid, a `401 Unauthorized` response is returned.

## API Reference

### Authentication & Authorization

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/auth/signup` | No | Register a new user |
| `POST` | `/auth/login` | No | Login and obtain JWT tokens |
| `POST` | `/auth/logout` | **Yes** | Invalidate the current session |
| `GET` | `/public/info` | No | Public endpoint test |
| `GET` | `/protected/profile`| **Yes** | Get current authenticated user profile |
| `GET` | `/protected/dashboard`| **Yes** | Get current user's dashboard |

### Tasks

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/tasks` | No | Retrieve all tasks |
| `POST` | `/tasks` | No | Create a new task |
| `GET` | `/tasks/{id}`| No | Retrieve a task by ID |
| `PUT` | `/tasks/{id}`| No | Update an existing task |
| `DELETE`| `/tasks/{id}`| No | Delete a task |

## Swagger Documentation

FastAPI's Swagger UI automatically integrates with the `HTTPBearer` security scheme. You can click the "Authorize" button (lock icon) to input your JWT token, and all protected endpoints will automatically include it in requests.

![Swagger UI](swagger_auth_screenshot.jpg)

## Testing

A testing pipeline script is provided for verifying layered architecture behavior. To run the automated validation tests:
```bash
python scratch/test_a3_pipeline.py
```

## Project Structure

```text
TaskAPI/
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── dependencies.py      # get_current_user dependency
│   │   └── supabase.py          # Supabase client instantiation
│   ├── database/
│   │   ├── models/
│   │   └── connection.py
│   ├── repositories/
│   │   ├── interface.py
│   │   └── postgres.py
│   ├── routes/
│   │   ├── auth.py              # Auth endpoints (login, signup)
│   │   ├── protected.py         # Protected endpoints
│   │   ├── public.py            # Public endpoints
│   │   └── tasks.py             # Task endpoints
│   ├── schemas/
│   │   ├── auth.py              # Pydantic schemas for Auth
│   │   └── task.py
│   ├── services/
│   │   └── task_service.py
│   └── main.py                  # FastAPI application & lifespan
├── compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```
