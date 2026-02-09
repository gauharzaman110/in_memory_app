from sqlmodel import create_engine, Session, SQLModel
import os
from models import Task, User  # Import all models

# Use a local SQLite database for development if DATABASE_URL is not set.
# The official database is Neon Serverless PostgreSQL.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# The connect_args are only for SQLite.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

