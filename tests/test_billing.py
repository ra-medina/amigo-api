from datetime import datetime

import pytest


@pytest.fixture(scope="module")
def billing_id(client):
    billing_payload = {
        "amount": 100.0,
        "date": datetime.now().isoformat(),
        "paid": False,
        "user_id": 11,
    }
    response = client.post("/billings/", json=billing_payload)
    assert response.status_code == 201, f"Response body is: {response.json()}"
    response_data = response.json()
    billing_id = response_data["id"]
    yield billing_id


def test_create_billing(billing_id):
    assert billing_id is not None, "Billing creation failed"


def test_get_billing(client, billing_id):
    response = client.get(f"/billings/{billing_id}")
    assert response.status_code == 200, f"Billing not found or error: {response.json()}"


def test_update_billing(client, billing_id):
    updated_data = {
        "amount": 150.0,
        "date": datetime.now().isoformat(),
        "paid": True,
    }
    response = client.put(f"/billings/{billing_id}", json=updated_data)
    assert response.status_code == 200, f"Update failed or error: {response.json()}"
    assert response.json()["amount"] == 150.0
    assert response.json()["paid"] is True


def test_delete_billing(client, billing_id):
    response = client.delete(f"/billings/{billing_id}")
    assert response.status_code == 204, f"Deletion failed or error: {response.json()}"

    response = client.get(f"/billings/{billing_id}")
    assert (
        response.status_code == 404
    ), "Billing should be deleted but is still accessible"
