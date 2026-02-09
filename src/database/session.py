from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
from .models import User, Task
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(bind=engine)