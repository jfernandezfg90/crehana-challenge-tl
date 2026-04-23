from uuid import UUID

from app.domain.entities.task import Task
from app.domain.exceptions.domain_exceptions import (
    InvalidTaskStatusTransitionException,
    TaskNotFoundException,
)
from app.domain.repositories.task_repository import TaskRepository
from app.domain.value_objects.task_status import TaskStatus

VALID_TRANSITIONS = {
    TaskStatus.PENDING: {TaskStatus.IN_PROGRESS},
    TaskStatus.IN_PROGRESS: {TaskStatus.DONE, TaskStatus.PENDING},
    TaskStatus.DONE: {TaskStatus.IN_PROGRESS},
}


class ChangeTaskStatusUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(
        self, task_id: UUID, task_list_id: UUID, new_status: TaskStatus
    ) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if not task or task.task_list_id != task_list_id:
            raise TaskNotFoundException(str(task_id))

        allowed = VALID_TRANSITIONS.get(task.status, set())
        if new_status not in allowed:
            raise InvalidTaskStatusTransitionException(
                task.status.value, new_status.value
            )

        task.status = new_status
        return self.task_repository.update(task)
