from datetime import datetime
from amigo.models import Billing, User


def create_test_user(db_session):
    user = User(email="user@test.com", full_name="Test User", hashed_password="test")
    db_session.add(user)
    db_session.commit()
    return user


def create_test_billing(db_session, user_id):
    billing = Billing(amount=100.0, date=datetime.now(), paid=False, user_id=user_id)
    db_session.add(billing)
    db_session.commit()
    return billing


def test_create_billing(client, db_session):
    user = create_test_user(db_session)
    billing_data = {
        "amount": 200.0,
        "date": datetime.now().isoformat(),
        "paid": False,
        "user_id": user.id,
    }
    response = client.post("/billings/", json=billing_data)
    assert response.status_code == 201, f"Failed to create billing: {response.json()}"


def test_get_billing(client, db_session):
    user = create_test_user(db_session)
    billing = create_test_billing(db_session, user.id)

    response = client.get(f"/billings/{billing.id}")
    assert response.status_code == 200, f"Billing not found: {response.json()}"


def test_update_billing(client, db_session):
    user = create_test_user(db_session)
    billing = create_test_billing(db_session, user.id)

    update_data = {"amount": 300.0, "paid": True}
    response = client.put(f"/billings/{billing.id}", json=update_data)
    assert response.status_code == 200, f"Update failed: {response.json()}"


def test_delete_billing(client, db_session):
    user = create_test_user(db_session)
    billing = create_test_billing(db_session, user.id)

    response = client.delete(f"/billings/{billing.id}")
    assert response.status_code == 204, f"Deletion failed: {response.json()}"
