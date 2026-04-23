import pytest


@pytest.fixture
def task_list_id(client, auth_headers):
    resp = client.post(
        "/api/v1/task-lists",
        json={"name": "Test List"},
        headers=auth_headers,
    )
    return resp.json()["id"]


def test_create_task(client, auth_headers, task_list_id):
    response = client.post(
        f"/api/v1/task-lists/{task_list_id}/tasks",
        json={"title": "My Task", "description": "Do it", "priority": "HIGH"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Task"
    assert data["status"] == "PENDING"
    assert data["priority"] == "HIGH"


def test_list_tasks_with_completion(client, auth_headers, task_list_id):
    client.post(
        f"/api/v1/task-lists/{task_list_id}/tasks",
        json={"title": "Task 1"},
        headers=auth_headers,
    )
    client.post(
        f"/api/v1/task-lists/{task_list_id}/tasks",
        json={"title": "Task 2"},
        headers=auth_headers,
    )

    response = client.get(
        f"/api/v1/task-lists/{task_list_id}/tasks",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert "completion_percentage" in data
    assert "total" in data
    assert data["completion_percentage"] == 0.0


def test_get_task(client, auth_headers, task_list_id):
    create_resp = client.post(
        f"/api/v1/task-lists/{task_list_id}/tasks",
        json={"title": "Get Me"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]
    response = client.get(
        f"/api/v1/task-lists/{task_list_id}/tasks/{task_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Get Me"


def test_update_task(client, auth_headers, task_list_id):
    create_resp = client.post(
        f"/api/v1/task-lists/{task_list_id}/tasks",
        json={"title": "Old"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]
    response = client.put(
        f"/api/v1/task-lists/{task_list_id}/tasks/{task_id}",
        json={"title": "Updated"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_change_task_status(client, auth_headers, task_list_id):
    create_resp = client.post(
        f"/api/v1/task-lists/{task_list_id}/tasks",
        json={"title": "Status Task"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]
    response = client.patch(
        f"/api/v1/task-lists/{task_list_id}/tasks/{task_id}/status",
        json={"status": "IN_PROGRESS"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"


def test_invalid_status_transition(client, auth_headers, task_list_id):
    create_resp = client.post(
        f"/api/v1/task-lists/{task_list_id}/tasks",
        json={"title": "Bad Transition"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]
    response = client.patch(
        f"/api/v1/task-lists/{task_list_id}/tasks/{task_id}/status",
        json={"status": "DONE"},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_filter_tasks_by_priority(client, auth_headers, task_list_id):
    client.post(
        f"/api/v1/task-lists/{task_list_id}/tasks",
        json={"title": "High", "priority": "HIGH"},
        headers=auth_headers,
    )
    client.post(
        f"/api/v1/task-lists/{task_list_id}/tasks",
        json={"title": "Low", "priority": "LOW"},
        headers=auth_headers,
    )
    response = client.get(
        f"/api/v1/task-lists/{task_list_id}/tasks?priority=HIGH",
        headers=auth_headers,
    )
    assert response.status_code == 200
    tasks = response.json()["tasks"]
    assert all(t["priority"] == "HIGH" for t in tasks)


def test_delete_task(client, auth_headers, task_list_id):
    create_resp = client.post(
        f"/api/v1/task-lists/{task_list_id}/tasks",
        json={"title": "Delete Me"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]
    response = client.delete(
        f"/api/v1/task-lists/{task_list_id}/tasks/{task_id}",
        headers=auth_headers,
    )
    assert response.status_code == 204
