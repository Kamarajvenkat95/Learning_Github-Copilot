"""
Constants and configuration for the application.
"""

from typing import Dict, Any

# Email validation
VALID_EMAIL_DOMAIN = "mergington.edu"
MIN_EMAIL_LENGTH = 5
MAX_EMAIL_LENGTH = 254

# Activity constraints
MIN_ACTIVITY_NAME_LENGTH = 2
MAX_ACTIVITY_NAME_LENGTH = 100
MIN_DESCRIPTION_LENGTH = 10
MAX_DESCRIPTION_LENGTH = 500

# Participant constraints
MIN_PARTICIPANTS = 0
MAX_PARTICIPANTS_LIMIT = 100

# Initial activities database
INITIAL_ACTIVITIES: Dict[str, Any] = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Team-based soccer practice and competitive matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["luke@mergington.edu", "mia@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Improve basketball skills and scrimmage with classmates",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and mixed media art projects",
        "schedule": "Mondays and Wednesdays, 3:45 PM - 5:15 PM",
        "max_participants": 14,
        "participants": ["harper@mergington.edu", "isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, stage production, and performance workshops",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["liam@mergington.edu", "emma@mergington.edu"]
    },
    "Science Club": {
        "description": "Experiment with science projects and prepare for competitions",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["oliver@mergington.edu", "amelia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["ethan@mergington.edu", "charlotte@mergington.edu"]
    }
}
