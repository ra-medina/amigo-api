import uuid
from datetime import datetime
from amigo.models import User, Billing


def create_test_user(db_session):
    user = User(
        email=f"test-{uuid.uuid4()}@example.com",
        full_name="Test User",
        hashed_password="test",
    )
    db_session.add(user)
    db_session.commit()
    return user


def create_test_billing(db_session, user):
    billing = Billing(amount=100.0, date=datetime.now(), paid=False, user_id=user.id)
    db_session.add(billing)
    db_session.commit()
    return billing


def test_create_billing(client, db_session):
    user = create_test_user(
        db_session
    )  # Ensure this function commits the user to the DB

    # Now use the user.id from the created user
    billing_data = {
        "amount": 100.0,
        "date": datetime.now().isoformat(),
        "paid": False,
        "user_id": user.id,
    }
    response = client.post("/billings/", json=billing_data)
    assert response.status_code == 201, f"Response body is: {response.json()}"
    assert response.json()["user_id"] == user.id


def test_get_billing(client, db_session):
    user = create_test_user(db_session)
    billing = create_test_billing(db_session, user)

    response = client.get(f"/billings/{billing.id}")
    assert response.status_code == 200, "Billing not found or error: {}".format(
        response.json()
    )


def test_update_billing(client, db_session):
    user = create_test_user(db_session)
    billing = create_test_billing(db_session, user)

    updated_data = {
        "amount": 150.0,
        "date": datetime.now().isoformat(),  # Ensure 'date' field is present if it's required
        "paid": True,
    }
    response = client.put(f"/billings/{billing.id}", json=updated_data)
    assert response.status_code == 200, "Update failed or error: {}".format(
        response.json()
    )


def test_delete_billing(client, db_session):
    user = create_test_user(db_session)
    billing = create_test_billing(db_session, user)

    response = client.delete(f"/billings/{billing.id}")
    assert response.status_code == 204, "Deletion failed or error: {}".format(
        response.json()
    )

    response = client.get(f"/billings/{billing.id}")
    assert response.status_code == 404, "Billing should be deleted but still accessible"
