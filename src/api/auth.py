from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
from .database.session import get_db
from .models.user_task import UserCreate, UserResponse, Token
from .services.user_service import UserService
from .utils.auth import create_access_token
from .utils.security import verify_password
from datetime import timedelta
import os

router = APIRouter()


@router.post("/auth/register", response_model=UserResponse)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        db_user = UserService.create_user(db, user_create)
        return UserResponse.from_orm(db_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/auth/login", response_model=Token)
def login(email: str, password: str, db: Session = Depends(get_db)):
    """Login with email and password to get JWT token"""
    user = UserService.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/logout")
def logout():
    """Logout the current user (client-side operation)"""
    return {"message": "Successfully logged out"}