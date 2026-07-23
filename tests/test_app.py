import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
from src.services.activity_service import ActivityService

client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activity_participants():
    """Restore activities to original state after each test."""
    original_participants = {
        name: details["participants"].copy() for name, details in activities.items()
    }
    yield
    for name, participants in original_participants.items():
        activities[name]["participants"] = participants.copy()


class TestGetActivities:
    """Tests for retrieving activities."""

    def test_get_activities_success(self):
        """Test successfully retrieving all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
        assert isinstance(data["Chess Club"]["participants"], list)

    def test_get_activities_has_required_fields(self):
        """Test that activities have all required fields."""
        response = client.get("/activities")
        data = response.json()
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data

    def test_get_specific_activity(self):
        """Test getting a specific activity."""
        response = client.get("/activities/Chess%20Club")
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Learn strategies and compete in chess tournaments"

    def test_get_nonexistent_activity(self):
        """Test getting a non-existent activity returns 404."""
        response = client.get("/activities/NonExistent")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestSignupForActivity:
    """Tests for signing up for activities."""

    def test_signup_new_participant_success(self):
        """Test successfully signing up a new participant."""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert "newstudent@mergington.edu" in response.json()["message"]

    def test_signup_verifies_participant_added(self):
        """Test that participant is actually added after signup."""
        test_email = "teststudent@mergington.edu"
        client.post(
            "/activities/Chess%20Club/signup",
            params={"email": test_email}
        )
        refreshed = client.get("/activities").json()
        assert test_email in refreshed["Chess Club"]["participants"]

    def test_signup_duplicate_participant_fails(self):
        """Test that signing up twice fails."""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_invalid_email_domain(self):
        """Test that email outside mergington.edu domain is rejected."""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "student@example.com"}
        )
        assert response.status_code == 400
        assert "mergington.edu" in response.json()["detail"].lower()

    def test_signup_invalid_email_format(self):
        """Test that invalid email format is rejected."""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "invalid-email"}
        )
        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()

    def test_signup_nonexistent_activity(self):
        """Test signing up for non-existent activity fails."""
        response = client.post(
            "/activities/NonExistent/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_empty_email(self):
        """Test that empty email is rejected."""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": ""}
        )
        assert response.status_code == 422  # Validation error

    def test_signup_capacity_full(self):
        """Test that signup fails when activity is at capacity."""
        # Create an activity with max_participants = 2 and 2 participants
        test_activity = "Test Activity"
        activities[test_activity] = {
            "description": "Test",
            "schedule": "Test",
            "max_participants": 1,
            "participants": ["existing@mergington.edu"]
        }
        
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 400
        assert "capacity" in response.json()["detail"].lower()


class TestRemoveParticipant:
    """Tests for removing participants."""

    def test_remove_participant_success(self):
        """Test successfully removing a participant."""
        response = client.delete(
            "/activities/Chess%20Club/participants",
            params={"email": "michael@mergington.edu"},
        )
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]

    def test_remove_participant_verifies_removal(self):
        """Test that participant is actually removed."""
        email = "michael@mergington.edu"
        client.delete(
            "/activities/Chess%20Club/participants",
            params={"email": email},
        )
        refreshed = client.get("/activities").json()
        assert email not in refreshed["Chess Club"]["participants"]

    def test_remove_nonexistent_participant(self):
        """Test removing non-existent participant fails."""
        response = client.delete(
            "/activities/Chess%20Club/participants",
            params={"email": "nonexistent@mergington.edu"},
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_remove_from_nonexistent_activity(self):
        """Test removing from non-existent activity fails."""
        response = client.delete(
            "/activities/NonExistent/participants",
            params={"email": "student@mergington.edu"},
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_remove_invalid_email_format(self):
        """Test removing with invalid email format fails."""
        response = client.delete(
            "/activities/Chess%20Club/participants",
            params={"email": "invalid-email"},
        )
        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
