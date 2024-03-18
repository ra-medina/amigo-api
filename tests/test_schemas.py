from amigo.schemas import UserCreate, AppointmentCreate, MedicalRecordCreate, NoteCreate
from datetime import datetime


def test_user_create_schema():
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "strongpassword",
    }
    user = UserCreate(**user_data)
    assert user.email == user_data["email"]
    assert user.full_name == user_data["full_name"]
    assert user.password == user_data["password"]


def test_appointment_create_schema():
    appointment_data = {
        "user_id": 1,
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "description": "Initial Consultation",
    }
    appointment = AppointmentCreate(**appointment_data)
    assert appointment.start_time == appointment_data["start_time"]
    assert appointment.end_time == appointment_data["end_time"]
    assert appointment.description == appointment_data["description"]


def test_medical_record_create_schema():
    record_data = {"record": "Patient has a history of migraines."}
    medical_record = MedicalRecordCreate(**record_data)
    assert medical_record.record == record_data["record"]


def test_note_create_schema():
    note_data = {"content": "Follow up in two weeks.", "created_at": datetime.now()}
    note = NoteCreate(**note_data)
    assert note.content == note_data["content"]
    assert note.created_at == note_data["created_at"]
