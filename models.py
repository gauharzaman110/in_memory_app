from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
import datetime
from typing import List

class User(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    # Relationship to tasks, if you want to define it here
    # tasks: List["Task"] = Relationship(back_populates="owner")

class Task(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, nullable=False)  # Change to int to match User.id
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    due_date: Optional[datetime.datetime] = None

    # Relationship to user
    # owner: User = Relationship(back_populates="tasks")