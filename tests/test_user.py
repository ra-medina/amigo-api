import uuid


def test_create_user(client):
    unique_email = f"test-{uuid.uuid4()}@example.com"
    user_data = {
        "email": unique_email,
        "full_name": "Test User",
        "phone_number": "123-456-7890",
        "role": "patient",
        "password": "testpass",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201, f"Response body is: {response.json()}"


def test_get_user(client):
    user_id = 1
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert "email" in data
    assert "full_name" in data
