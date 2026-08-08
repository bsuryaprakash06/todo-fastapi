from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.database.models.task import TaskModel

class TaskRepositoryInterface(ABC):
    @abstractmethod
    def get_all(self, search: Optional[str] = None, done: Optional[bool] = None, sort: bool = False) -> List[TaskModel]:
        """Retrieve all tasks with optional search, filter, and sort."""
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[TaskModel]:
        """Retrieve a single task by its integer ID."""
        pass

    @abstractmethod
    def create(self, title: str, done: bool = False) -> TaskModel:
        """Create and persist a new task."""
        pass

    @abstractmethod
    def update(self, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[TaskModel]:
        """Update an existing task."""
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted, False if not found."""
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, int]:
        """Retrieve task statistics (total, completed, pending)."""
        pass
