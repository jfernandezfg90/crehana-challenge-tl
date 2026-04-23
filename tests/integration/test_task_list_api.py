def test_create_task_list(client, auth_headers):
    response = client.post(
        "/api/v1/task-lists",
        json={"name": "My List", "description": "Test list"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My List"
    assert data["description"] == "Test list"
    assert "id" in data


def test_list_task_lists(client, auth_headers):
    client.post(
        "/api/v1/task-lists",
        json={"name": "List A"},
        headers=auth_headers,
    )
    response = client.get("/api/v1/task-lists", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_task_list(client, auth_headers):
    create_resp = client.post(
        "/api/v1/task-lists",
        json={"name": "Detail List"},
        headers=auth_headers,
    )
    list_id = create_resp.json()["id"]
    response = client.get(f"/api/v1/task-lists/{list_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Detail List"


def test_get_task_list_not_found(client, auth_headers):
    import uuid

    response = client.get(f"/api/v1/task-lists/{uuid.uuid4()}", headers=auth_headers)
    assert response.status_code == 404


def test_update_task_list(client, auth_headers):
    create_resp = client.post(
        "/api/v1/task-lists",
        json={"name": "Old Name"},
        headers=auth_headers,
    )
    list_id = create_resp.json()["id"]
    response = client.put(
        f"/api/v1/task-lists/{list_id}",
        json={"name": "New Name"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_delete_task_list(client, auth_headers):
    create_resp = client.post(
        "/api/v1/task-lists",
        json={"name": "To Delete"},
        headers=auth_headers,
    )
    list_id = create_resp.json()["id"]
    response = client.delete(f"/api/v1/task-lists/{list_id}", headers=auth_headers)
    assert response.status_code == 204

    get_resp = client.get(f"/api/v1/task-lists/{list_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_requires_auth(client):
    response = client.get("/api/v1/task-lists")
    assert response.status_code in (401, 403)
