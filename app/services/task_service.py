from typing import List, Optional, Dict
from app.repositories.interface import TaskRepositoryInterface
from app.database.models.task import TaskModel

class TaskNotFoundError(Exception):
    """Domain exception raised when a task is not found."""
    pass

class InvalidTaskTitleError(ValueError):
    """Domain exception raised when a task title is blank or invalid."""
    pass

class TaskService:
    def __init__(self, repository: TaskRepositoryInterface):
        self.repository = repository

    def get_all_tasks(
        self,
        search: Optional[str] = None,
        done: Optional[bool] = None,
        sort: bool = False
    ) -> List[TaskModel]:
        normalized_search = search.strip() if search else None
        return self.repository.get_all(search=normalized_search, done=done, sort=sort)

    def get_task_by_id(self, task_id: int) -> TaskModel:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
        return task

    def create_task(self, title: str, done: bool = False) -> TaskModel:
        normalized_title = title.strip() if title else ""
        if not normalized_title:
            raise InvalidTaskTitleError("Title cannot be empty")
        return self.repository.create(title=normalized_title, done=done)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        done: Optional[bool] = None
    ) -> TaskModel:
        # Check existence first
        self.get_task_by_id(task_id)

        normalized_title = None
        if title is not None:
            normalized_title = title.strip()
            if not normalized_title:
                raise InvalidTaskTitleError("Title cannot be empty")

        updated = self.repository.update(task_id=task_id, title=normalized_title, done=done)
        if not updated:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
        return updated

    def delete_task(self, task_id: int) -> None:
        deleted = self.repository.delete(task_id)
        if not deleted:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

    def get_stats(self) -> Dict[str, int]:
        return self.repository.get_stats()
