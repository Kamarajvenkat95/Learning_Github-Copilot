import pytest

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activity_participants():
    original_participants = {
        name: details["participants"].copy() for name, details in activities.items()
    }
    yield
    for name, participants in original_participants.items():
        activities[name]["participants"] = participants.copy()


def test_get_activities():
    response = client.get("/activities")

    assert response.status_code == 200

    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_new_participant():
    response = client.post("/activities/Chess%20Club/signup", params={"email": "teststudent@mergington.edu"})

    assert response.status_code == 200
    assert "Successfully signed up teststudent@mergington.edu for Chess Club" in response.json()["message"]

    refreshed = client.get("/activities").json()
    assert "teststudent@mergington.edu" in refreshed["Chess Club"]["participants"]


def test_signup_duplicate_participant():
    response = client.post("/activities/Chess%20Club/signup", params={"email": "michael@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_remove_participant():
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert "Successfully removed michael@mergington.edu from Chess Club" in response.json()["message"]

    refreshed = client.get("/activities").json()
    assert "michael@mergington.edu" not in refreshed["Chess Club"]["participants"]


def test_remove_missing_participant():
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "unknown@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
