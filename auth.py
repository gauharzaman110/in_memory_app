# backend/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from datetime import datetime, timedelta
from typing import Optional, Annotated

from sqlmodel import Session, select
from db import get_session
from models import User # Import User model

# --- Configuration ---
# This should be the same secret key used by Better Auth on the frontend.
# In a real application, this MUST be stored securely in an environment variable.
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "a_very_secret_key_that_should_be_changed")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Default expiry for access tokens

# This scheme will look for a token in the 'Authorization: Bearer <token>' header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)]
) -> User:
    """
    Decodes the JWT token to get the user, and fetches the user from the database.
    This will be the dependency that protects our routes.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
            
        user = session.get(User, user_id)
        if user is None:
            raise credentials_exception
        return user
        
    except (JWTError, ValueError): # Add ValueError for int conversion errors
        raise credentials_exception
