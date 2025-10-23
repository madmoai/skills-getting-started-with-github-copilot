import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
    ("Programming Class", "coder@mergington.edu"),
])
def test_signup_and_unregister(activity, email):
    # Signup
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200
    assert f"Signed up {email}" in signup.json()["message"]
    # Unregister
    unregister = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister.status_code == 200
    assert f"Unregistered {email}" in unregister.json()["message"]


def test_signup_duplicate():
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Already signed up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]


def test_unregister_not_signed_up():
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 400
    assert "not registered" in resp.json()["detail"]
