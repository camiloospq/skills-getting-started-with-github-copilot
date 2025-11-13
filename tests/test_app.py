import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code in (200, 400)  # 400 if already signed up
    # Unregister
    resp2 = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code in (200, 404)  # 404 if not found

def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    activity = "Programming Class"
    # First signup
    resp1 = client.post(f"/activities/{activity}/signup?email={email}")
    # Second signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400
    assert "already signed up" in resp2.json().get("detail", "")
    # Cleanup
    client.delete(f"/activities/{activity}/signup?email={email}")

def test_unregister_not_found():
    email = "notfound@mergington.edu"
    activity = "Gym Class"
    resp = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "")
