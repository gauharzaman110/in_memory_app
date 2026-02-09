from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from db import create_db_and_tables
from routes import tasks, auth, chat

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# --- Local User Storage (for development/testing) ---
class LocalUser(BaseModel):
    email: str
    hashed_password: str

def get_local_db():
    db = sqlite3.connect('local_users.db')
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # Create local user storage table
    with sqlite3.connect('local_users.db') as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL
            )
        """)

# Include API routers
app.include_router(tasks.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
