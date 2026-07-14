"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

from src.constants import INITIAL_ACTIVITIES
from src.services.activity_service import ActivityService
from src.routes import activities as activities_routes

app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Initialize activities database
activities = {name: details.copy() for name, details in INITIAL_ACTIVITIES.items()}

# Initialize activity service
activity_service = ActivityService(activities)
activities_routes.set_service(activity_service)

# Include activity routes
app.include_router(activities_routes.router)


@app.get(
    "/",
    summary="Root endpoint",
    description="Redirect to the web application"
)
def root():
    """Redirect to the main web application."""
    return RedirectResponse(url="/static/index.html")


@app.get(
    "/health",
    summary="Health check",
    description="Check if the API is running",
    tags=["health"]
)
def health_check():
    """Health check endpoint.
    
    Returns:
        Status indicator
    """
    return {"status": "healthy", "version": "1.0.0"}
