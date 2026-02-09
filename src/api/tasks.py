from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .api.dependencies import get_current_user, get_db
from .database.models import User
from .models.user_task import TaskResponse, TaskCreate, TaskUpdate
from .services.task_service import TaskService

router = APIRouter()


@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all tasks for the authenticated user"""
    tasks = TaskService.get_tasks(db, current_user.id)
    return tasks


@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task for the authenticated user"""
    db_task = TaskService.create_task(db, task_create, current_user.id)
    return db_task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task for the authenticated user"""
    task = TaskService.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a specific task for the authenticated user"""
    task = TaskService.update_task(db, task_id, task_update, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific task for the authenticated user"""
    success = TaskService.delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}