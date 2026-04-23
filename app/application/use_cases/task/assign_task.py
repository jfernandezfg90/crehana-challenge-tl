"""
Caso de Uso: Asignar Tarea.
Asigna una tarea a un usuario y dispara notificaciones.
"""

from uuid import UUID

from app.application.services.notification_service import NotificationService
from app.domain.entities.task import Task
from app.domain.exceptions.domain_exceptions import (
    TaskNotFoundException,
    UserNotFoundException,
)
from app.domain.repositories.task_repository import TaskRepository
from app.domain.repositories.user_repository import UserRepository


class AssignTaskUseCase:
    def __init__(
        self,
        task_repository: TaskRepository,
        user_repository: UserRepository,
        notification_service: NotificationService,
    ):
        self.task_repository = task_repository
        self.user_repository = user_repository
        self.notification_service = notification_service

    def execute(self, task_id: UUID, task_list_id: UUID, user_id: UUID) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if not task or task.task_list_id != task_list_id:
            raise TaskNotFoundException(str(task_id))

        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(str(user_id))

        task.assigned_user_id = user_id
        updated_task = self.task_repository.update(task)

        self.notification_service.send_assignment_notification(
            user_email=user.email,
            task_title=task.title,
        )

        return updated_task
