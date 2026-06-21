from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities_state():
    original_state = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities_returns_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_then_unregister_participant(client):
    activity_name = "Chess Club"
    email = "pytest-student@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )
    assert unregister_response.status_code == 200
