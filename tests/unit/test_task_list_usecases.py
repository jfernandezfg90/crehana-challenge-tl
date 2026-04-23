from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.application.use_cases.task_list.create_task_list import CreateTaskListUseCase
from app.application.use_cases.task_list.delete_task_list import DeleteTaskListUseCase
from app.application.use_cases.task_list.get_task_list import GetTaskListUseCase
from app.application.use_cases.task_list.update_task_list import UpdateTaskListUseCase
from app.domain.entities.task_list import TaskList
from app.domain.exceptions.domain_exceptions import (
    TaskListNotFoundException,
    UnauthorizedAccessException,
)


def make_task_list(owner_id=None):
    return TaskList(name="My List", owner_id=owner_id or uuid4())


class TestCreateTaskList:
    def test_creates_and_returns_task_list(self):
        repo = MagicMock()
        owner_id = uuid4()
        tl = make_task_list(owner_id)
        repo.create.return_value = tl

        result = CreateTaskListUseCase(repo).execute("My List", owner_id)

        repo.create.assert_called_once()
        assert result.name == "My List"

    def test_passes_description(self):
        repo = MagicMock()
        owner_id = uuid4()
        tl = TaskList(name="L", owner_id=owner_id, description="desc")
        repo.create.return_value = tl

        result = CreateTaskListUseCase(repo).execute("L", owner_id, description="desc")
        assert result.description == "desc"


class TestGetTaskList:
    def test_returns_task_list(self):
        repo = MagicMock()
        owner_id = uuid4()
        tl = make_task_list(owner_id)
        repo.get_by_id.return_value = tl

        result = GetTaskListUseCase(repo).execute(tl.id, owner_id)
        assert result == tl

    def test_raises_not_found(self):
        repo = MagicMock()
        repo.get_by_id.return_value = None

        with pytest.raises(TaskListNotFoundException):
            GetTaskListUseCase(repo).execute(uuid4(), uuid4())

    def test_raises_unauthorized(self):
        repo = MagicMock()
        tl = make_task_list()
        repo.get_by_id.return_value = tl

        with pytest.raises(UnauthorizedAccessException):
            GetTaskListUseCase(repo).execute(tl.id, uuid4())

    def test_get_all_by_owner(self):
        repo = MagicMock()
        owner_id = uuid4()
        repo.get_all_by_owner.return_value = [make_task_list(owner_id)]

        results = GetTaskListUseCase(repo).execute_all(owner_id)
        assert len(results) == 1


class TestUpdateTaskList:
    def test_updates_name(self):
        repo = MagicMock()
        owner_id = uuid4()
        tl = make_task_list(owner_id)
        repo.get_by_id.return_value = tl
        repo.update.return_value = tl

        UpdateTaskListUseCase(repo).execute(tl.id, owner_id, name="New Name")
        assert tl.name == "New Name"

    def test_raises_not_found(self):
        repo = MagicMock()
        repo.get_by_id.return_value = None

        with pytest.raises(TaskListNotFoundException):
            UpdateTaskListUseCase(repo).execute(uuid4(), uuid4(), name="X")

    def test_raises_unauthorized(self):
        repo = MagicMock()
        tl = make_task_list()
        repo.get_by_id.return_value = tl

        with pytest.raises(UnauthorizedAccessException):
            UpdateTaskListUseCase(repo).execute(tl.id, uuid4(), name="X")


class TestDeleteTaskList:
    def test_deletes(self):
        repo = MagicMock()
        owner_id = uuid4()
        tl = make_task_list(owner_id)
        repo.get_by_id.return_value = tl

        DeleteTaskListUseCase(repo).execute(tl.id, owner_id)
        repo.delete.assert_called_once_with(tl.id)

    def test_raises_not_found(self):
        repo = MagicMock()
        repo.get_by_id.return_value = None

        with pytest.raises(TaskListNotFoundException):
            DeleteTaskListUseCase(repo).execute(uuid4(), uuid4())

    def test_raises_unauthorized(self):
        repo = MagicMock()
        tl = make_task_list()
        repo.get_by_id.return_value = tl

        with pytest.raises(UnauthorizedAccessException):
            DeleteTaskListUseCase(repo).execute(tl.id, uuid4())
