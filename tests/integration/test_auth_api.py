def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "new@example.com", "password": "secret123", "name": "New User"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert data["name"] == "New User"
    assert "id" in data


def test_register_duplicate_email(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "pass", "name": "A"},
    )
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "pass", "name": "B"},
    )
    assert response.status_code == 409


def test_login_success(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "pass123", "name": "L"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "pass123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "pw@example.com", "password": "correct", "name": "P"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "pw@example.com", "password": "wrong"},
    )
    assert response.status_code == 401


def test_login_unknown_email(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "pass"},
    )
    assert response.status_code == 401
