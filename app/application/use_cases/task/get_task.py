from uuid import UUID

from app.domain.entities.task import Task
from app.domain.exceptions.domain_exceptions import TaskNotFoundException
from app.domain.repositories.task_repository import TaskRepository


class GetTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, task_id: UUID, task_list_id: UUID) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if not task or task.task_list_id != task_list_id:
            raise TaskNotFoundException(str(task_id))
        return task
