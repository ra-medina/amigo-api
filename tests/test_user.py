def test_create_user(client):
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpass",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data


def test_get_user(client, db):
    user_id = 1  # Assuming a user with this ID exists in the test DB
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert "email" in data
    assert "full_name" in data
