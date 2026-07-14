"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class ActivityResponse(BaseModel):
    """Response model for a single activity."""
    description: str
    schedule: str
    max_participants: int
    participants: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
            }
        }


class SignupRequest(BaseModel):
    """Request model for signing up for an activity."""
    email: EmailStr = Field(..., description="Student email address")
    activity_name: str = Field(..., description="Name of the activity to sign up for")


class ParticipantRemovalRequest(BaseModel):
    """Request model for removing a participant."""
    email: EmailStr = Field(..., description="Student email address")
    activity_name: str = Field(..., description="Name of the activity")


class SuccessResponse(BaseModel):
    """Generic success response."""
    message: str


class ErrorResponse(BaseModel):
    """Generic error response."""
    detail: str


class ActivitiesResponse(BaseModel):
    """Response model for all activities."""
    __root__: dict[str, ActivityResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "Chess Club": {
                    "description": "Learn strategies and compete in chess tournaments",
                    "schedule": "Fridays, 3:30 PM - 5:00 PM",
                    "max_participants": 12,
                    "participants": ["michael@mergington.edu"]
                }
            }
        }
