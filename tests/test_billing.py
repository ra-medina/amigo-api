from datetime import datetime
from amigo.models import User


def create_test_user(db_session):
    user = User(email="user@test.com", full_name="Test User", hashed_password="test")
    db_session.add(user)
    db_session.commit()
    return user


def test_create_billing(client, db_session):
    # Setup: create a user to associate with the billing
    user = create_test_user(db_session)

    billing_data = {
        "amount": 100.0,
        "date": datetime.now().isoformat(),
        "paid": False,
        "user_id": user.id,
    }
    response = client.post("/billings/", json=billing_data)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == billing_data["amount"]
    assert data["user_id"] == user.id


def test_get_billing(client, db_session):
    # Setup: create a user and a billing record
    user = create_test_user(db_session)
    billing = create_test_billing(db_session, user.id)

    response = client.get(f"/billings/{billing.id}")
    assert response.status_code == 200
    assert response.json()["id"] == billing.id


def test_update_billing(client, db_session):
    # Setup: create a user and a billing record
    user = create_test_user(db_session)
    billing = create_test_billing(db_session, user.id)

    updated_data = {"amount": 150.0, "paid": True}
    response = client.put(f"/billings/{billing.id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == updated_data["amount"]
    assert data["paid"] == updated_data["paid"]


def test_delete_billing(client, db_session):
    # Setup: create a user and a billing record
    user = create_test_user(db_session)
    billing = create_test_billing(db_session, user.id)

    response = client.delete(f"/billings/{billing.id}")
    assert response.status_code == 204

    # Verify that the billing record has been deleted
    response = client.get(f"/billings/{billing.id}")
    assert response.status_code == 404


# Helper function to create a billing record for testing
def create_test_billing(db_session, user_id):
    from amigo.models import Billing

    billing = Billing(amount=100.0, date=datetime.now(), paid=False, user_id=user_id)
    db_session.add(billing)
    db_session.commit()
    return billing
