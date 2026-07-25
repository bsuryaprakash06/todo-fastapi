from fastapi import FastAPI, HTTPException
from typing import List, Optional
from app.database import get_db_connection
from app.schemas import Task, TaskCreate, TaskUpdate

app = FastAPI()

@app.get("/", summary="Root Endpoint", description="Returns a welcome message.")
def read_root():
    return {"message": "Welcome to Todo API"}

@app.get("/health", summary="Health Check", description="Returns the server health status.")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", response_model=List[Task], summary="Get All Tasks", description="Retrieves a list of all tasks. Optionally filter by a search string or completion status, and sort alphabetically.")
def get_tasks(search: Optional[str] = None, done: Optional[bool] = None, sort: bool = False):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    
    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")
        
    if done is not None:
        query += " AND done = ?"
        params.append(1 if done else 0)
        
    if sort:
        query += " ORDER BY title"
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/stats", summary="Get Task Statistics", description="Returns total, completed, and pending task counts.")
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1")
    completed = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 0")
    pending = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }

@app.get("/tasks/{task_id}", response_model=Task, summary="Get Task by ID", description="Retrieves a specific task by its integer ID.")
def get_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    return dict(row)

@app.post("/tasks", response_model=Task, status_code=201, summary="Create Task", description="Creates a new task. The title is required and cannot be empty or just whitespace.")
def create_task(task_in: TaskCreate):
    title = task_in.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, 0))
    new_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (new_id,))
    new_task = cursor.fetchone()
    conn.close()
    
    return dict(new_task)

@app.put("/tasks/{task_id}", response_model=Task, summary="Update Task", description="Updates an existing task's title and/or completion status.")
def update_task(task_id: int, task_in: TaskUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
    current_title = row["title"]
    current_done = row["done"]
    
    if task_in.title is not None:
        title = task_in.title.strip()
        if not title:
            conn.close()
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        current_title = title
        
    if task_in.done is not None:
        current_done = task_in.done
        
    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (current_title, current_done, task_id))
    conn.commit()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    updated_task = cursor.fetchone()
    conn.close()
    
    return dict(updated_task)

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete Task", description="Deletes a task permanently.")
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
        
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return None
