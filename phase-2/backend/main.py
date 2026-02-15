"""
Phase II Full-Stack Web Application - Backend
FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.db import create_db_tables
from routes import auth, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan event handler.

    Creates database tables on startup.
    """
    # Startup: Create tables
    create_db_tables()
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="Todo API - Phase II",
    description="Multi-user todo application with JWT authentication",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS Configuration - Allow frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API status check"""
    return {
        "message": "Todo API Phase II is running",
        "version": "2.0.0",
        "status": "active"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}


# Register routers
app.include_router(auth.router)
app.include_router(tasks.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
