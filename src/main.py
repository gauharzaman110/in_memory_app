from fastapi import FastAPI
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.api.middleware import add_cors_middleware
from src.database.session import create_db_and_tables


def create_app():
    app = FastAPI(title="Todo API", version="1.0.0")

    # Add middleware
    add_cors_middleware(app)

    # Include routers
    app.include_router(auth_router)
    app.include_router(tasks_router)

    # Create database tables
    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    # Health check endpoint
    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)