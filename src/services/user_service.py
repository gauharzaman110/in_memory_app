from sqlmodel import Session, select
from typing import Optional
from .database.models import User
from .utils.security import get_password_hash, verify_password
from .models.user_task import UserCreate


class UserService:
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user with hashed password"""
        # Check if user already exists
        existing_user = db.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = db.exec(select(User).where(User.email == email)).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.get(User, user_id)