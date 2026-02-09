from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Annotated
from datetime import timedelta

from db import get_session
from models import User
from auth import SECRET_KEY, ALGORITHM, create_access_token, get_current_user
from passlib.context import CryptContext
from jose import jwt

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/signup")
async def signup(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)]
):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(form_data.password)
    new_user = User(email=form_data.username, hashed_password=hashed_password)
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    access_token_expires = timedelta(minutes=30) # You can adjust this
    access_token = create_access_token(
        data={"sub": str(new_user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": new_user.id, "email": new_user.email}}

@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)]
):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, # Use 404 for user not found
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password", # More specific error
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30) # You can adjust this
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": user.id, "email": user.email}}

@router.post("/logout")
async def logout():
    # On the backend, logout is essentially just returning a success.
    # The client is responsible for discarding the token.
    return {"message": "Logout successful"}

@router.get("/session")
async def get_session_info(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return {"user": {"id": current_user.id, "email": current_user.email}}