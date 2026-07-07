import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as _activities


initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
}


@pytest.fixture(autouse=True)
def reset_activities():
    # reset the in-memory activities dict before each test
    _activities.clear()
    _activities.update(copy.deepcopy(initial_activities))
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
