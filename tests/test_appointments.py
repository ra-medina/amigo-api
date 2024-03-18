import pytest
from datetime import datetime, timedelta
from amigo.models import User, Appointment


@pytest.fixture
def test_user(db_session):
    user = User(
        email=f"user-{datetime.now().isoformat()}@test.com",
        full_name="Test User",
        hashed_password="test",
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_appointment(db_session, test_user):
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    appointment = Appointment(
        start_time=start_time,
        end_time=end_time,
        description="Test Appointment",
        user_id=test_user.id,
    )
    db_session.add(appointment)
    db_session.commit()
    return appointment


def test_create_appointment(client, test_user):
    appointment_data = {
        "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        "description": "Test Create Appointment",
        "user_id": test_user.id,
    }
    response = client.post("/appointments/", json=appointment_data)
    assert response.status_code == 201
    assert response.json()["description"] == "Test Create Appointment"


def test_get_appointments(client, test_appointment):
    response = client.get("/appointments/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_appointment(client, test_appointment):
    response = client.get(f"/appointments/{test_appointment.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_appointment.id


def test_update_appointment(client, test_appointment):
    updated_data = {
        "description": "Updated Test Appointment",
        "start_time": test_appointment.start_time.isoformat(),
        "end_time": test_appointment.end_time.isoformat(),
        "user_id": test_appointment.user_id,
    }
    response = client.put(f"/appointments/{test_appointment.id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["description"] == "Updated Test Appointment"


def test_delete_appointment(client, test_appointment):
    response = client.delete(f"/appointments/{test_appointment.id}")
    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/appointments/{test_appointment.id}")
    assert response.status_code == 404
