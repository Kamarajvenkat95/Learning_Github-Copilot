"""
API routes for activity management.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any
from src.services.activity_service import ActivityService
from src.models import SuccessResponse, ActivityResponse, ErrorResponse

router = APIRouter(
    prefix="/activities",
    tags=["activities"],
    responses={404: {"model": ErrorResponse}}
)

# Initialize service (will be injected from main app)
activity_service: ActivityService = None


def set_service(service: ActivityService) -> None:
    """Set the activity service instance.
    
    Args:
        service: ActivityService instance
    """
    global activity_service
    activity_service = service


@router.get(
    "",
    response_model=Dict[str, ActivityResponse],
    summary="Get all activities",
    description="Retrieve all available extracurricular activities with their details and participant information"
)
def get_activities():
    """Get all activities with participant information.
    
    Returns:
        Dictionary of all activities
    """
    if activity_service is None:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    return activity_service.get_activities()


@router.get(
    "/{activity_name}",
    response_model=ActivityResponse,
    summary="Get a specific activity",
    description="Retrieve details for a specific activity"
)
def get_activity(activity_name: str):
    """Get a specific activity by name.
    
    Args:
        activity_name: Name of the activity
        
    Returns:
        Activity details
    """
    if activity_service is None:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    return activity_service.get_activity(activity_name)


@router.post(
    "/{activity_name}/signup",
    response_model=SuccessResponse,
    status_code=200,
    summary="Sign up for an activity",
    description="Register a student for an extracurricular activity",
    responses={
        400: {"model": ErrorResponse, "description": "Validation error or already signed up"},
        404: {"model": ErrorResponse, "description": "Activity not found"},
    }
)
def signup_for_activity(
    activity_name: str,
    email: str = Query(..., description="Student email address")
):
    """Sign up a student for an activity.
    
    Args:
        activity_name: Name of the activity
        email: Email of the student
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If signup validation fails
    """
    if activity_service is None:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    return activity_service.signup_participant(activity_name, email)


@router.delete(
    "/{activity_name}/participants",
    response_model=SuccessResponse,
    status_code=200,
    summary="Remove a participant",
    description="Unregister a student from an activity",
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        404: {"model": ErrorResponse, "description": "Activity or participant not found"},
    }
)
def remove_participant(
    activity_name: str,
    email: str = Query(..., description="Student email address")
):
    """Remove a participant from an activity.
    
    Args:
        activity_name: Name of the activity
        email: Email of the student
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If removal validation fails
    """
    if activity_service is None:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    return activity_service.remove_participant(activity_name, email)
