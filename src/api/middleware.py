from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app: FastAPI):
    """Add CORS middleware to allow frontend communication"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify your frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )