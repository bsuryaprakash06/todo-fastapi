from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)

class TaskCreate(TaskBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries"
                }
            ]
        }
    }

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    done: Optional[bool] = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries and milk",
                    "done": True
                }
            ]
        }
    }

class Task(TaskBase):
    id: int
    done: bool
