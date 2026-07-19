from fastapi import FastAPI, HTTPException
from typing import List
from app.data import tasks
from app.helpers import get_task_by_id
from app.schemas import Task

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Todo API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
