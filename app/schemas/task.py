from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, description="Title of the task")
    done: bool = Field(default=False, description="Completion status of the task")

class TaskCreate(BaseModel):
    title: str = Field(..., description="Title of the task (required, non-empty)")
    done: bool = Field(default=False, description="Completion status of the task")

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, description="Updated title of the task")
    done: Optional[bool] = Field(default=None, description="Updated completion status")

class Task(TaskBase):
    id: int = Field(..., description="Unique integer ID of the task")

    model_config = ConfigDict(from_attributes=True)
