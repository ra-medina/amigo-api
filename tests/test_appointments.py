import pytest
from datetime import datetime, timedelta
from amigo.schemas import AppointmentCreate
from amigo.models import Appointment, User


def create_test_user(db_session):
    user = User(email="user@test.com", full_name="Test User", hashed_password="test")
    db_session.add(user)
    db_session.commit()
    return user


def test_create_appointment(client, db_session):
    user = create_test_user(db_session)
    start_time = datetime.now().isoformat()
    end_time = (datetime.now() + timedelta(hours=1)).isoformat()

    appointment_data = {
        "start_time": start_time,
        "end_time": end_time,
        "description": "Test Appointment",
        "user_id": user.id,
    }
    response = client.post("/appointments/", json=appointment_data)
    assert (
        response.status_code == 201
    ), f"Failed to create appointment: {response.json()}"


def test_get_appointment(client, db_session):
    user = create_test_user(db_session)
    appointment = Appointment(
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=1),
        description="Test Appointment",
        user_id=user.id,
    )
    db_session.add(appointment)
    db_session.commit()

    response = client.get(f"/appointments/{appointment.id}")
    assert response.status_code == 200, f"Appointment not found: {response.json()}"


def test_update_appointment(client, db_session):
    user = create_test_user(db_session)
    appointment = Appointment(
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=1),
        description="Initial Appointment",
        user_id=user.id,
    )
    db_session.add(appointment)
    db_session.commit()

    update_data = {"description": "Updated Appointment"}
    response = client.put(f"/appointments/{appointment.id}", json=update_data)
    assert response.status_code == 200, f"Update failed: {response.json()}"


def test_delete_appointment(client, db_session):
    user = create_test_user(db_session)
    appointment = Appointment(
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=1),
        description="Delete Appointment",
        user_id=user.id,
    )
    db_session.add(appointment)
    db_session.commit()

    response = client.delete(f"/appointments/{appointment.id}")
    assert response.status_code == 204, f"Deletion failed: {response.json()}"
