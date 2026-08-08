from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.repositories.postgres import PostgresTaskRepository
from app.services.task_service import (
    TaskService,
    TaskNotFoundError,
    InvalidTaskTitleError
)
from app.schemas.task import Task, TaskCreate, TaskUpdate

router = APIRouter()

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    repository = PostgresTaskRepository(db)
    return TaskService(repository)

@router.get("/", summary="Root Endpoint", description="Returns a welcome message.")
def read_root():
    return {"message": "Welcome to Todo API"}

@router.get("/health", summary="Health Check", description="Returns server health status.")
def health_check():
    return {"status": "ok"}

@router.get(
    "/tasks",
    response_model=List[Task],
    summary="Get All Tasks",
    description="Retrieves a list of all tasks. Optionally search, filter by completion status, and sort alphabetically."
)
def get_tasks(
    search: Optional[str] = None,
    done: Optional[bool] = None,
    sort: bool = False,
    service: TaskService = Depends(get_task_service)
):
    return service.get_all_tasks(search=search, done=done, sort=sort)

@router.get(
    "/stats",
    summary="Get Task Statistics",
    description="Returns total, completed, and pending task counts."
)
def get_stats(service: TaskService = Depends(get_task_service)) -> Dict[str, int]:
    return service.get_stats()

@router.get(
    "/tasks/{task_id}",
    response_model=Task,
    summary="Get Task by ID",
    description="Retrieves a specific task by its integer ID."
)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    try:
        return service.get_task_by_id(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@router.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create Task",
    description="Creates a new task with a required, non-empty title."
)
def create_task(
    task_in: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    try:
        return service.create_task(title=task_in.title, done=task_in.done)
    except InvalidTaskTitleError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put(
    "/tasks/{task_id}",
    response_model=Task,
    summary="Update Task",
    description="Updates an existing task's title and/or completion status."
)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    try:
        return service.update_task(task_id=task_id, title=task_in.title, done=task_in.done)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except InvalidTaskTitleError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Task",
    description="Deletes a task permanently."
)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    try:
        service.delete_task(task_id)
        return None
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
