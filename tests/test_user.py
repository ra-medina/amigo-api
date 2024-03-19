import pytest


# Creating a pytest fixture for the test user.
# We remove this test user if all tests are ran succesfully.
@pytest.fixture(scope="module")
def user_id(client):
    user_data = {
        "email": "testing2@ugly.com",
        "full_name": "Test User",
        "phone_number": "123-456-7890",
        "role": "patient",
        "password": "testpass",
        "is_active": False,
        "is_clinician": False,
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201, f"Response body is: {response.json()}"
    user_data = response.json()
    return user_data["id"]


def test_get_user(client, user_id):
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_update_user(client, user_id):
    update_payload = {"email": "cant_see_me@example.com"}
    response = client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["email"] == "cant_see_me@example.com"


def test_delete_user(client, user_id):
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
