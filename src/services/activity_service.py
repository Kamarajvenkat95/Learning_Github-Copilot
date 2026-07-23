"""
Business logic service for activity management.
"""

from typing import Dict, List, Any, Optional
from fastapi import HTTPException
from src.constants import (
    VALID_EMAIL_DOMAIN,
    MIN_ACTIVITY_NAME_LENGTH,
    MAX_ACTIVITY_NAME_LENGTH,
    MAX_PARTICIPANTS_LIMIT,
)


class ActivityService:
    """Service for managing activities and participants."""

    def __init__(self, activities: Dict[str, Any]):
        """Initialize with activities database.
        
        Args:
            activities: Dictionary of activities with participant data
        """
        self.activities = activities

    def validate_activity_name(self, activity_name: str) -> None:
        """Validate activity name exists and is properly formatted.
        
        Args:
            activity_name: Name of the activity
            
        Raises:
            HTTPException: If activity name is invalid
        """
        if not activity_name or len(activity_name.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Activity name cannot be empty"
            )
        
        if len(activity_name) < MIN_ACTIVITY_NAME_LENGTH or len(activity_name) > MAX_ACTIVITY_NAME_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Activity name must be between {MIN_ACTIVITY_NAME_LENGTH} and {MAX_ACTIVITY_NAME_LENGTH} characters"
            )
        
        if activity_name not in self.activities:
            raise HTTPException(
                status_code=404,
                detail=f"Activity '{activity_name}' not found"
            )

    def validate_email(self, email: str) -> None:
        """Validate email format and domain.
        
        Args:
            email: Email address to validate
            
        Raises:
            HTTPException: If email is invalid
        """
        if not email or len(email.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Email cannot be empty"
            )
        
        # Basic email format check
        if "@" not in email:
            raise HTTPException(
                status_code=400,
                detail="Invalid email format"
            )
        
        domain = email.split("@")[-1].lower()
        if domain != VALID_EMAIL_DOMAIN:
            raise HTTPException(
                status_code=400,
                detail=f"Email must be from {VALID_EMAIL_DOMAIN} domain"
            )

    def validate_capacity(self, activity_name: str) -> None:
        """Validate that activity has available capacity.
        
        Args:
            activity_name: Name of the activity
            
        Raises:
            HTTPException: If activity is at capacity
        """
        activity = self.activities[activity_name]
        if len(activity["participants"]) >= activity["max_participants"]:
            raise HTTPException(
                status_code=400,
                detail=f"Activity '{activity_name}' is at full capacity"
            )

    def signup_participant(self, activity_name: str, email: str) -> Dict[str, str]:
        """Sign up a participant for an activity.
        
        Args:
            activity_name: Name of the activity
            email: Email of the participant
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If signup fails
        """
        # Validate inputs
        self.validate_activity_name(activity_name)
        self.validate_email(email)
        
        activity = self.activities[activity_name]
        
        # Check if already signed up
        if email in activity["participants"]:
            raise HTTPException(
                status_code=400,
                detail=f"Student {email} is already signed up for {activity_name}"
            )
        
        # Check capacity
        self.validate_capacity(activity_name)
        
        # Add participant
        activity["participants"].append(email)
        
        return {"message": f"Successfully signed up {email} for {activity_name}"}

    def remove_participant(self, activity_name: str, email: str) -> Dict[str, str]:
        """Remove a participant from an activity.
        
        Args:
            activity_name: Name of the activity
            email: Email of the participant
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If removal fails
        """
        # Validate inputs
        self.validate_activity_name(activity_name)
        self.validate_email(email)
        
        activity = self.activities[activity_name]
        
        # Check if participant exists
        if email not in activity["participants"]:
            raise HTTPException(
                status_code=404,
                detail=f"Participant {email} not found in {activity_name}"
            )
        
        # Remove participant
        activity["participants"].remove(email)
        
        return {"message": f"Successfully removed {email} from {activity_name}"}

    def get_activities(self) -> Dict[str, Any]:
        """Get all activities.
        
        Returns:
            Dictionary of all activities
        """
        return self.activities

    def get_activity(self, activity_name: str) -> Dict[str, Any]:
        """Get a specific activity.
        
        Args:
            activity_name: Name of the activity
            
        Returns:
            Activity details
            
        Raises:
            HTTPException: If activity not found
        """
        self.validate_activity_name(activity_name)
        return self.activities[activity_name]

    def get_available_spot_count(self, activity_name: str) -> int:
        """Get number of available spots in an activity.
        
        Args:
            activity_name: Name of the activity
            
        Returns:
            Number of available spots
            
        Raises:
            HTTPException: If activity not found
        """
        activity = self.get_activity(activity_name)
        return activity["max_participants"] - len(activity["participants"])
