import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    assert "already signed up" in response_dup.json()["detail"]


def test_remove_participant():
    email = "removeme@mergington.edu"
    activity = "Chess Club"
    # Ensure participant is present
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Removed")
    # Try removing again
    response_missing = client.delete(f"/activities/{activity}/participants/{email}")
    assert response_missing.status_code == 404
    assert "Participant not found" in response_missing.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=nouser@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_activity_not_found():
    response = client.delete("/activities/Nonexistent/participants/nouser@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
