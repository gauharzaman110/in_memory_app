from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database.session import SessionLocal
from .utils.auth import verify_token, security
from .database.models import User


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Dependency to get the current user from the JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token.credentials, credentials_exception)
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    
    return user