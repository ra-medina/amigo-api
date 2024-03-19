from datetime import datetime, timedelta

from amigo.models import Appointment, User


def test_create_user(db_session):
    email = "test@example.com"
    user = User(email=email, full_name="Test User", hashed_password="hashed_test_pass")
    db_session.add(user)
    db_session.commit()

    retrieved_user = db_session.query(User).filter_by(email=email).first()
    assert retrieved_user is not None
    assert retrieved_user.email == email


def test_create_appointment(db_session):
    user = User(
        email="user_for_appointment@example.com",
        full_name="Test User",
        hashed_password="hashed_pass",
    )
    db_session.add(user)
    db_session.commit()

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    appointment = Appointment(start_time=start_time, end_time=end_time, user_id=user.id)
    db_session.add(appointment)
    db_session.commit()

    retrieved_appointment = db_session.query(Appointment).filter_by(user_id=user.id).first()
    assert retrieved_appointment is not None
    assert retrieved_appointment.start_time == start_time
    assert retrieved_appointment.end_time == end_time
