import pytest
from datetime import datetime, timedelta
from amigo.models import Appointment


@pytest.fixture(scope="module")
def test_appointment(client):
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    appointment_data = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "description": "Test Appointment",
        "user_id": 11,
    }
    response = client.post("/appointments/", json=appointment_data)
    assert response.status_code == 201, f"Response body is: {response.json()}"
    appointment_data = response.json()
    return appointment_data["id"]


def test_create_appointment(client):
    appointment_payload = {
        "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        "description": "Test Create Appointment",
        "notes": "test note",
        "user_id": 11,
    }
    response = client.post("/appointments/", json=appointment_payload)
    assert response.status_code == 201
    assert response.json()["description"] == "Test Create Appointment"


def test_get_appointments(client):
    response = client.get("/appointments/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_appointment(client, test_appointment):
    response = client.get(f"/appointments/{test_appointment}")
    assert response.status_code == 200
    assert response.json()["id"] == test_appointment


def test_update_appointment(client, test_appointment):
    updated_data = {
        "description": "Updated Test Appointment",
        "start_time": test_appointment.start_time.isoformat(),
        "end_time": test_appointment.end_time.isoformat(),
        "user_id": test_appointment.user_id,
    }
    response = client.put(f"/appointments/{test_appointment}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["description"] == "Updated Test Appointment"


def test_delete_appointment(client, test_appointment):
    response = client.delete(f"/appointments/{test_appointment}")
    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/appointments/{test_appointment}")
    assert response.status_code == 404
