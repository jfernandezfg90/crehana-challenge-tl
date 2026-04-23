from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.application.use_cases.task.assign_task import AssignTaskUseCase
from app.application.use_cases.task.change_task_status import ChangeTaskStatusUseCase
from app.application.use_cases.task.create_task import CreateTaskUseCase
from app.application.use_cases.task.delete_task import DeleteTaskUseCase
from app.application.use_cases.task.get_task import GetTaskUseCase
from app.application.use_cases.task.list_tasks import ListTasksUseCase
from app.application.use_cases.task.update_task import UpdateTaskUseCase
from app.domain.entities.task import Task
from app.domain.entities.task_list import TaskList
from app.domain.entities.user import User
from app.domain.exceptions.domain_exceptions import (
    InvalidTaskStatusTransitionException,
    TaskListNotFoundException,
    TaskNotFoundException,
    UserNotFoundException,
)
from app.domain.value_objects.task_status import TaskStatus


def make_task(list_id=None, status=TaskStatus.PENDING):
    return Task(title="Task 1", task_list_id=list_id or uuid4(), status=status)


class TestCreateTask:
    def test_creates_task(self):
        task_repo = MagicMock()
        list_repo = MagicMock()
        owner_id = uuid4()
        list_id = uuid4()
        tl = TaskList(name="L", owner_id=owner_id)
        tl.id = list_id
        list_repo.get_by_id.return_value = tl
        task = make_task(list_id)
        task_repo.create.return_value = task

        result = CreateTaskUseCase(task_repo, list_repo).execute(
            "Task 1", list_id, owner_id
        )
        assert result.title == "Task 1"

    def test_raises_when_list_not_found(self):
        task_repo = MagicMock()
        list_repo = MagicMock()
        list_repo.get_by_id.return_value = None

        with pytest.raises(TaskListNotFoundException):
            CreateTaskUseCase(task_repo, list_repo).execute("T", uuid4(), uuid4())

    def test_raises_when_not_owner(self):
        task_repo = MagicMock()
        list_repo = MagicMock()
        tl = TaskList(name="L", owner_id=uuid4())
        list_repo.get_by_id.return_value = tl

        with pytest.raises(TaskListNotFoundException):
            CreateTaskUseCase(task_repo, list_repo).execute("T", tl.id, uuid4())


class TestGetTask:
    def test_returns_task(self):
        repo = MagicMock()
        list_id = uuid4()
        task = make_task(list_id)
        repo.get_by_id.return_value = task

        result = GetTaskUseCase(repo).execute(task.id, list_id)
        assert result == task

    def test_raises_not_found(self):
        repo = MagicMock()
        repo.get_by_id.return_value = None

        with pytest.raises(TaskNotFoundException):
            GetTaskUseCase(repo).execute(uuid4(), uuid4())

    def test_raises_wrong_list(self):
        repo = MagicMock()
        task = make_task()
        repo.get_by_id.return_value = task

        with pytest.raises(TaskNotFoundException):
            GetTaskUseCase(repo).execute(task.id, uuid4())


class TestUpdateTask:
    def test_updates_title(self):
        repo = MagicMock()
        list_id = uuid4()
        task = make_task(list_id)
        repo.get_by_id.return_value = task
        repo.update.return_value = task

        UpdateTaskUseCase(repo).execute(task.id, list_id, title="New Title")
        assert task.title == "New Title"

    def test_raises_not_found(self):
        repo = MagicMock()
        repo.get_by_id.return_value = None

        with pytest.raises(TaskNotFoundException):
            UpdateTaskUseCase(repo).execute(uuid4(), uuid4(), title="X")


class TestDeleteTask:
    def test_deletes(self):
        repo = MagicMock()
        list_id = uuid4()
        task = make_task(list_id)
        repo.get_by_id.return_value = task

        DeleteTaskUseCase(repo).execute(task.id, list_id)
        repo.delete.assert_called_once_with(task.id)

    def test_raises_not_found(self):
        repo = MagicMock()
        repo.get_by_id.return_value = None

        with pytest.raises(TaskNotFoundException):
            DeleteTaskUseCase(repo).execute(uuid4(), uuid4())


class TestChangeTaskStatus:
    def test_pending_to_in_progress(self):
        repo = MagicMock()
        list_id = uuid4()
        task = make_task(list_id, TaskStatus.PENDING)
        repo.get_by_id.return_value = task
        repo.update.return_value = task

        ChangeTaskStatusUseCase(repo).execute(task.id, list_id, TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS

    def test_invalid_transition_pending_to_done(self):
        repo = MagicMock()
        list_id = uuid4()
        task = make_task(list_id, TaskStatus.PENDING)
        repo.get_by_id.return_value = task

        with pytest.raises(InvalidTaskStatusTransitionException):
            ChangeTaskStatusUseCase(repo).execute(task.id, list_id, TaskStatus.DONE)

    def test_raises_not_found(self):
        repo = MagicMock()
        repo.get_by_id.return_value = None

        with pytest.raises(TaskNotFoundException):
            ChangeTaskStatusUseCase(repo).execute(uuid4(), uuid4(), TaskStatus.DONE)


class TestListTasks:
    def test_completion_percentage(self):
        repo = MagicMock()
        list_id = uuid4()
        tasks = [
            make_task(list_id, TaskStatus.DONE),
            make_task(list_id, TaskStatus.DONE),
            make_task(list_id, TaskStatus.PENDING),
            make_task(list_id, TaskStatus.PENDING),
        ]
        repo.get_all_by_list.return_value = tasks

        result = ListTasksUseCase(repo).execute(list_id)
        assert result.completion_percentage == 50.0
        assert result.total == 4

    def test_empty_list_returns_zero_percentage(self):
        repo = MagicMock()
        list_id = uuid4()
        repo.get_all_by_list.return_value = []

        result = ListTasksUseCase(repo).execute(list_id)
        assert result.completion_percentage == 0.0
        assert result.total == 0

    def test_all_done_returns_100(self):
        repo = MagicMock()
        list_id = uuid4()
        repo.get_all_by_list.return_value = [
            make_task(list_id, TaskStatus.DONE),
            make_task(list_id, TaskStatus.DONE),
        ]

        result = ListTasksUseCase(repo).execute(list_id)
        assert result.completion_percentage == 100.0


class TestAssignTask:
    def test_assigns_and_notifies(self):
        task_repo = MagicMock()
        user_repo = MagicMock()
        notification_svc = MagicMock()
        list_id = uuid4()
        user_id = uuid4()
        task = make_task(list_id)
        user = User(email="u@example.com", hashed_password="h", name="U")
        user.id = user_id
        task_repo.get_by_id.return_value = task
        user_repo.get_by_id.return_value = user
        task_repo.update.return_value = task

        AssignTaskUseCase(task_repo, user_repo, notification_svc).execute(
            task.id, list_id, user_id
        )

        assert task.assigned_user_id == user_id
        notification_svc.send_assignment_notification.assert_called_once()

    def test_raises_when_task_not_found(self):
        task_repo = MagicMock()
        task_repo.get_by_id.return_value = None

        with pytest.raises(TaskNotFoundException):
            AssignTaskUseCase(task_repo, MagicMock(), MagicMock()).execute(
                uuid4(), uuid4(), uuid4()
            )

    def test_raises_when_user_not_found(self):
        task_repo = MagicMock()
        user_repo = MagicMock()
        list_id = uuid4()
        task = make_task(list_id)
        task_repo.get_by_id.return_value = task
        user_repo.get_by_id.return_value = None

        with pytest.raises(UserNotFoundException):
            AssignTaskUseCase(task_repo, user_repo, MagicMock()).execute(
                task.id, list_id, uuid4()
            )
