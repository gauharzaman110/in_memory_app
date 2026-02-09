from sqlmodel import Session, select
from typing import List, Optional
from .database.models import Task, User
from .models.user_task import TaskCreate, TaskUpdate


class TaskService:
    @staticmethod
    def create_task(db: Session, task_create: TaskCreate, user_id: str) -> Task:
        """Create a new task for a user"""
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            is_completed=task_create.is_completed,
            user_id=user_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_tasks(db: Session, user_id: str) -> List[Task]:
        """Get all tasks for a specific user"""
        tasks = db.exec(select(Task).where(Task.user_id == user_id)).all()
        return tasks

    @staticmethod
    def get_task(db: Session, task_id: int, user_id: str) -> Optional[Task]:
        """Get a specific task for a user"""
        task = db.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()
        return task

    @staticmethod
    def update_task(db: Session, task_id: int, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        """Update a specific task for a user"""
        db_task = TaskService.get_task(db, task_id, user_id)
        if not db_task:
            return None
        
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int, user_id: str) -> bool:
        """Delete a specific task for a user"""
        db_task = TaskService.get_task(db, task_id, user_id)
        if not db_task:
            return False
        
        db.delete(db_task)
        db.commit()
        return True