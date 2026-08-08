from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.repositories.interface import TaskRepositoryInterface
from app.database.models.task import TaskModel

class PostgresTaskRepository(TaskRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, search: Optional[str] = None, done: Optional[bool] = None, sort: bool = False) -> List[TaskModel]:
        query = self.db.query(TaskModel)
        if search:
            query = query.filter(TaskModel.title.ilike(f"%{search}%"))
        if done is not None:
            query = query.filter(TaskModel.done == done)
        if sort:
            query = query.order_by(TaskModel.title.asc())
        return query.all()

    def get_by_id(self, task_id: int) -> Optional[TaskModel]:
        return self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

    def create(self, title: str, done: bool = False) -> TaskModel:
        task = TaskModel(title=title, done=done)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[TaskModel]:
        task = self.get_by_id(task_id)
        if not task:
            return None
        if title is not None:
            task.title = title
        if done is not None:
            task.done = done
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True

    def get_stats(self) -> Dict[str, int]:
        total = self.db.query(func.count(TaskModel.id)).scalar() or 0
        completed = self.db.query(func.count(TaskModel.id)).filter(TaskModel.done == True).scalar() or 0
        pending = self.db.query(func.count(TaskModel.id)).filter(TaskModel.done == False).scalar() or 0
        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }
