from typing import Dict, Optional
from app.data import tasks

def get_task_by_id(task_id: int) -> Optional[Dict]:
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def generate_new_id() -> int:
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1
