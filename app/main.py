from fastapi import FastAPI, HTTPException
from typing import List, Optional
from app.data import tasks
from app.helpers import get_task_by_id, generate_new_id
from app.schemas import Task, TaskCreate, TaskUpdate

app = FastAPI()

@app.get("/", summary="Root Endpoint", description="Returns a welcome message.")
def read_root():
    return {"message": "Welcome to Todo API"}

@app.get("/health", summary="Health Check", description="Returns the server health status.")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", response_model=List[Task], summary="Get All Tasks", description="Retrieves a list of all tasks. Optionally filter by a search string.")
def get_tasks(search: Optional[str] = None):
    if search:
        return [t for t in tasks if search.lower() in t["title"].lower()]
    return tasks

@app.get("/stats", summary="Get Task Statistics", description="Returns total, completed, and pending task counts.")
def get_stats():
    total = len(tasks)
    completed = sum(1 for t in tasks if t["done"])
    pending = total - completed
    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }

@app.get("/tasks/{task_id}", response_model=Task, summary="Get Task by ID", description="Retrieves a specific task by its integer ID.")
def get_task(task_id: int):
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=Task, status_code=201, summary="Create Task", description="Creates a new task. The title is required and cannot be empty or just whitespace.")
def create_task(task_in: TaskCreate):
    title = task_in.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    new_task = {
        "id": generate_new_id(),
        "title": title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task, summary="Update Task", description="Updates an existing task's title and/or completion status.")
def update_task(task_id: int, task_in: TaskUpdate):
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_in.title is not None:
        title = task_in.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        task["title"] = title
        
    if task_in.done is not None:
        task["done"] = task_in.done
        
    return task

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete Task", description="Deletes a task permanently.")
def delete_task(task_id: int):
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(task)
    return None
