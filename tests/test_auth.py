def test_register_user(client):
    response = client.post(
        "/register", json={"email": "test@example.com", "password": "secret123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_email(client):
    client.post("/register", json={"email": "dup@example.com", "password": "secret123"})
    response = client.post(
        "/register", json={"email": "dup@example.com", "password": "secret123"}
    )
    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/register", json={"email": "login@example.com", "password": "secret123"}
    )
    response = client.post(
        "/login",
        data={"username": "login@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/register", json={"email": "wrong@example.com", "password": "secret123"}
    )
    response = client.post(
        "/login",
        data={"username": "wrong@example.com", "password": "badpassword"},
    )
    assert response.status_code == 401
