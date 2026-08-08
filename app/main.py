from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.connection import init_db
from app.routes.tasks import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed initial data if empty
    init_db()
    yield

app = FastAPI(
    title="Todo API",
    description="A lightweight RESTful API for managing tasks with clean layered architecture, PostgreSQL, and Docker Compose.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(tasks_router)
