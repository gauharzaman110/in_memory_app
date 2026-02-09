# backend/routes/tasks.py (updated with authentication)
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel, Field
from typing import List, Optional, Union, Annotated
import datetime

from db import get_session
from models import Task, User
from auth import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    due_date: Optional[datetime.datetime] = None

class TaskRead(SQLModel):
    id: int
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    due_date: Optional[datetime.datetime] = None

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    due_date: Optional[datetime.datetime] = None


@router.get("/tasks", response_model=List[TaskRead])
def read_tasks(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
    completed: Optional[bool] = None,
    sort: Optional[str] = None # Added sort parameter
):
    query = select(Task).where(Task.user_id == current_user.id)
    if completed is not None:
        query = query.where(Task.completed == completed)
    
    # Add sorting logic
    if sort == "created":
        query = query.order_by(Task.created_at)
    elif sort == "title":
        query = query.order_by(Task.title)
    elif sort == "due_date":
        query = query.order_by(Task.due_date)
    # Default sorting (e.g., by created_at descending) can be added here if desired
    else:
        query = query.order_by(Task.created_at.desc()) # Default sort to most recent first

    tasks = session.exec(query).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskRead)
def read_task_by_id(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)]
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this task")
    return task

@router.post("/tasks", response_model=TaskRead)
def create_task(
    *,
    session: Session = Depends(get_session),
    task: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)]
):
    db_task = Task(**task.model_dump(), user_id=current_user.id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    print(f"Task created: '{db_task.title}' by user '{current_user.email}'")
    return db_task

@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    task: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_user)]
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    db_task.updated_at = datetime.datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    print(f"Task updated: '{db_task.title}' by user '{current_user.email}'")
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)]
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    
    print(f"Task deleted: '{db_task.title}' by user '{current_user.email}'")
    session.delete(db_task)
    session.commit()
    return {"ok": True, "deleted_task": db_task}

@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def complete_task(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)]
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to complete this task")

    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
