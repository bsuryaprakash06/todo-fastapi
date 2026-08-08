# Todo FastAPI

A production-ready RESTful API for managing tasks built with FastAPI and PostgreSQL, featuring a layered architecture (Route → Service → Repository → Database), request validation with Pydantic, and multi-container orchestration using Docker Compose.

## Architecture Overview

The application is structured into decoupled layers following clean architecture principles and containerized using Docker Compose:

```text
                        Docker Compose
                              │
               ┌──────────────┴──────────────┐
               │                             │
               ▼                             ▼
        FastAPI Container              PostgreSQL Container
               │                             │
               ▼                             ▼
        routes/tasks.py                 tasks table
               │                             │
               ▼                             │
        services/task_service.py             │
               │                             │
               ▼                             │
      repositories/postgres.py ──────────────┘
                                             │
                                             ▼
                                    Named Docker Volume
                                      (postgres_data)
```

### Layer Responsibilities

- **Routes (`app/routes/tasks.py`)**: Handles HTTP requests, parameter extraction, response serialization, status codes, and translates domain errors to HTTP exceptions.
- **Service (`app/services/task_service.py`)**: Implements business rules, validation, input normalization (e.g. whitespace trimming), and domain exceptions (`TaskNotFoundError`, `InvalidTaskTitleError`). Independent of HTTP/FastAPI.
- **Repository (`app/repositories/`)**: Abstract interface (`interface.py`) and PostgreSQL implementation (`postgres.py`) encapsulating database access via SQLAlchemy.
- **Database (`app/database/`)**: Database connection, session management (`connection.py`), and SQLAlchemy ORM models (`models/task.py`).

## Features

- Complete CRUD operations for task management
- Search tasks by keyword (`GET /tasks?search=...`)
- Filter tasks by completion status (`GET /tasks?done=true`)
- Sort tasks alphabetically (`GET /tasks?sort=true`)
- Task statistics endpoint (`GET /stats`)
- Request validation and serialization using Pydantic
- Automatic database table creation and safe initial seeding
- Persistent data storage using Docker named volumes
- Interactive OpenAPI (Swagger UI) documentation

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL 16 (Alpine)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Containerization**: Docker & Docker Compose
- **Server**: Uvicorn

## Quick Start with Docker Compose

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

### Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/bsuryaprakash06/todo-fastapi.git
   cd todo-fastapi
   ```

2. Start the services with Docker Compose:
   ```bash
   docker compose up --build
   ```

   Docker Compose will:
   - Build the FastAPI container image.
   - Start the PostgreSQL container (`todo_postgres_db`).
   - Create and mount the persistent volume `postgres_data`.
   - Wait for the database healthcheck to pass before starting the FastAPI app (`todo_fastapi_app`).
   - Automatically initialize tables and seed 3 sample tasks.

3. The API will be available at:
   - API Root: `http://127.0.0.1:8000`
   - Interactive Swagger Docs: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

4. To stop the containers:
   ```bash
   docker compose down
   ```

   To stop and remove persistent volumes:
   ```bash
   docker compose down -v
   ```

## Local Development (Without Docker)

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set the `DATABASE_URL` environment variable:
   ```bash
   # Example:
   export DATABASE_URL="postgresql://<user>:<password>@localhost:5432/<dbname>"
   ```

4. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

| Method | Endpoint | Description | Query Parameters / Body |
|--------|----------|-------------|-------------------------|
| `GET` | `/` | Welcome message | None |
| `GET` | `/health` | Server health check | None |
| `GET` | `/tasks` | Retrieve all tasks | `search` (str), `done` (bool), `sort` (bool) |
| `GET` | `/tasks/{id}` | Retrieve task by ID | `id` (int, path) |
| `POST` | `/tasks` | Create a new task | Body: `{"title": "...", "done": false}` |
| `PUT` | `/tasks/{id}` | Update an existing task | Body: `{"title": "...", "done": true}` |
| `DELETE` | `/tasks/{id}` | Delete a task | `id` (int, path) |
| `GET` | `/stats` | Task count statistics | None |

## Project Structure

```text
TaskAPI/
├── app/
│   ├── database/
│   │   ├── models/
│   │   │   └── task.py          # SQLAlchemy ORM TaskModel
│   │   └── connection.py        # Engine, SessionLocal, init_db
│   ├── repositories/
│   │   ├── interface.py         # TaskRepositoryInterface (ABC)
│   │   └── postgres.py          # PostgresTaskRepository (SQLAlchemy)
│   ├── routes/
│   │   └── tasks.py             # FastAPI APIRouter & HTTP handlers
│   ├── schemas/
│   │   └── task.py              # Pydantic schemas (Task, TaskCreate, TaskUpdate)
│   ├── services/
│   │   └── task_service.py      # Business logic & domain errors
│   └── main.py                  # FastAPI application & lifespan
├── compose.yml                  # Docker Compose configuration
├── Dockerfile                   # FastAPI container build instructions
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
└── README.md                    # Project documentation
```

## License

This project is licensed under the MIT License.
